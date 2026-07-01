from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import JournalEntry


def count_words(text: str) -> int:
    stripped = text.strip()
    if not stripped:
        return 0
    return len(stripped.split())


async def create_entry(
    session: AsyncSession,
    *,
    user_id: UUID,
    title: str | None,
    body: str,
) -> JournalEntry:
    entry = JournalEntry(
        user_id=user_id,
        title=title,
        body=body,
        word_count=count_words(body),
        reflection_completed=False,
    )
    session.add(entry)
    await session.flush()
    await session.refresh(entry)
    return entry


async def list_entries_for_user(
    session: AsyncSession,
    user_id: UUID,
    *,
    limit: int = 20,
    before: datetime | None = None,
) -> list[JournalEntry]:
    q = select(JournalEntry).where(JournalEntry.user_id == user_id)
    if before is not None:
        q = q.where(JournalEntry.created_at < before)
    q = q.order_by(JournalEntry.created_at.desc()).limit(limit)
    result = await session.execute(q)
    return list(result.scalars().all())


async def get_entry_for_user(
    session: AsyncSession, user_id: UUID, entry_id: UUID
) -> JournalEntry | None:
    result = await session.execute(
        select(JournalEntry).where(
            JournalEntry.id == entry_id,
            JournalEntry.user_id == user_id,
        )
    )
    return result.scalar_one_or_none()