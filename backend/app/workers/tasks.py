from uuid import UUID

from app.core.deps import SessionLocal
from app.workers.pipeline import run_entry_intelligence_pipeline


async def enqueue_entry_pipeline(user_id: UUID, entry_id: UUID) -> None:
    async with SessionLocal() as session:
        await run_entry_intelligence_pipeline(
            session,
            user_id=user_id,
            entry_id=entry_id,
        )