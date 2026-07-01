from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.logging import get_logger
from app.db.models import AnalysisJob, JobStatus
from app.growth.projection import project_tree, record_depth_signal
from app.intelligence.analysis import analyze_entry
from app.intelligence.extraction import extract_memories
from app.journal.service import get_entry_for_user
from app.memories.service import create_memory_with_embedding

logger = get_logger(__name__)


async def _job_start(session: AsyncSession, user_id: UUID, entry_id: UUID, job_type: str) -> AnalysisJob:
    job = AnalysisJob(
        user_id=user_id,
        entry_id=entry_id,
        job_type=job_type,
        status=JobStatus.running,
    )
    session.add(job)
    await session.flush()
    return job


async def _job_done(session: AsyncSession, job: AnalysisJob, *, error: str | None = None) -> None:
    from datetime import datetime, timezone

    job.status = JobStatus.failed if error else JobStatus.completed
    job.error = error
    job.completed_at = datetime.now(timezone.utc)
    await session.flush()


async def run_entry_intelligence_pipeline(
    session: AsyncSession,
    *,
    user_id: UUID,
    entry_id: UUID,
) -> None:
    settings = get_settings()
    entry = await get_entry_for_user(session, user_id, entry_id)
    if entry is None:
        return

    analysis_job = await _job_start(session, user_id, entry_id, "analysis")
    analysis = None
    depth_mag = 0.0
    for attempt in range(2):
        try:
            analysis = await analyze_entry(entry.body, entry.title, settings)
            entry.depth_score = analysis["depth_score"]
            depth_mag = await record_depth_signal(
                session, user_id, entry_id, analysis["depth_score"]
            )
            await _job_done(session, analysis_job)
            break
        except Exception as exc:
            if attempt == 1:
                logger.error("analysis_failed", entry_id=str(entry_id), error=str(exc))
                await _job_done(session, analysis_job, error=str(exc))
                await session.commit()
                return

    assert analysis is not None
    extract_job = await _job_start(session, user_id, entry_id, "extract")
    created = 0
    try:
        items = await extract_memories(
            entry.body,
            entry.title,
            analysis.get("themes", []),
            settings,
        )
        for item in items:
            mem = await create_memory_with_embedding(
                session,
                user_id=user_id,
                source_entry_id=entry_id,
                first_mentioned_at=entry.created_at,
                item=item,
                settings=settings,
            )
            if mem:
                created += 1
        await _job_done(session, extract_job)
    except Exception as exc:
        logger.error("extract_failed", entry_id=str(entry_id), error=str(exc))
        await _job_done(session, extract_job, error=str(exc))

    try:
        await project_tree(session, user_id, depth_delta=depth_mag)
    except Exception as exc:
        logger.error("tree_project_failed", user_id=str(user_id), error=str(exc))

    await session.commit()
    logger.info(
        "pipeline_complete",
        entry_id=str(entry_id),
        memories_created=created,
        depth_score=entry.depth_score,
    )