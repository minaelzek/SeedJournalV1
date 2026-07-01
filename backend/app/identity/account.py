from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import (
    AnalysisJob,
    GrowthEvent,
    JournalEntry,
    Memory,
    RefreshToken,
    ReflectionSession,
    ReflectionTurn,
    TreeState,
    User,
)
from app.db.models_vector import MemoryEmbedding


async def export_user_data(session: AsyncSession, user_id: UUID) -> dict:
    user = await session.get(User, user_id)
    if user is None or user.deleted_at is not None:
        return {}

    entries = (
        await session.execute(select(JournalEntry).where(JournalEntry.user_id == user_id))
    ).scalars().all()
    memories = (
        await session.execute(select(Memory).where(Memory.user_id == user_id))
    ).scalars().all()
    tree = await session.get(TreeState, user_id)

    return {
        "user": {
            "id": str(user.id),
            "email": user.email,
            "timezone": user.timezone,
            "created_at": user.created_at.isoformat(),
        },
        "entries": [
            {
                "id": str(e.id),
                "title": e.title,
                "body": e.body,
                "created_at": e.created_at.isoformat(),
            }
            for e in entries
        ],
        "memories": [
            {
                "id": str(m.id),
                "type": m.type.value,
                "title": m.title,
                "summary": m.summary,
                "first_mentioned_at": m.first_mentioned_at.isoformat(),
            }
            for m in memories
        ],
        "tree": {
            "stage": tree.stage.value if tree else "seed",
            "season": tree.season.value if tree else "spring",
        },
    }


async def delete_user_account(session: AsyncSession, user_id: UUID) -> bool:
    user = await session.get(User, user_id)
    if user is None:
        return False

    user.deleted_at = datetime.now(timezone.utc)

    memory_ids = list(
        (
            await session.execute(select(Memory.id).where(Memory.user_id == user_id))
        ).scalars().all()
    )
    if memory_ids:
        await session.execute(
            delete(MemoryEmbedding).where(MemoryEmbedding.memory_id.in_(memory_ids))
        )

    session_ids = list(
        (
            await session.execute(
                select(ReflectionSession.id).where(ReflectionSession.user_id == user_id)
            )
        ).scalars().all()
    )
    if session_ids:
        await session.execute(
            delete(ReflectionTurn).where(ReflectionTurn.session_id.in_(session_ids))
        )
        await session.execute(
            delete(ReflectionSession).where(ReflectionSession.id.in_(session_ids))
        )

    await session.execute(delete(AnalysisJob).where(AnalysisJob.user_id == user_id))
    await session.execute(delete(GrowthEvent).where(GrowthEvent.user_id == user_id))
    await session.execute(delete(Memory).where(Memory.user_id == user_id))
    await session.execute(delete(JournalEntry).where(JournalEntry.user_id == user_id))
    await session.execute(delete(TreeState).where(TreeState.user_id == user_id))
    await session.execute(delete(RefreshToken).where(RefreshToken.user_id == user_id))
    await session.flush()
    return True