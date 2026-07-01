from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import JournalEntry, Season, TreeState


async def apply_season_from_activity(session: AsyncSession, user_id, tree: TreeState) -> None:
    """Gentle season shifts — winter is rest, not punishment."""
    result = await session.execute(
        select(JournalEntry.created_at)
        .where(JournalEntry.user_id == user_id)
        .order_by(JournalEntry.created_at.desc())
        .limit(1)
    )
    last = result.scalar_one_or_none()
    if last is None:
        tree.season = Season.spring
        return

    now = datetime.now(timezone.utc)
    last_dt = last if last.tzinfo else last.replace(tzinfo=timezone.utc)
    days = (now - last_dt).days

    if days >= 45:
        tree.season = Season.winter
    elif days >= 21:
        tree.season = Season.autumn
    elif tree.leaves_count >= 8:
        tree.season = Season.summer
    else:
        tree.season = Season.spring