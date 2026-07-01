from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.growth.seasons import apply_season_from_activity
from app.db.models import GrowthEvent, JournalEntry, Memory, MemoryType, TreeStage, TreeState


def _stage_for_index(growth_index: float, has_flower: bool) -> TreeStage:
    if growth_index >= 0.70 and has_flower:
        return TreeStage.blooming
    if growth_index >= 0.45:
        return TreeStage.sakura
    if growth_index >= 0.22:
        return TreeStage.sapling
    if growth_index >= 0.08:
        return TreeStage.sprout
    return TreeStage.seed


async def project_tree(
    session: AsyncSession,
    user_id: UUID,
    *,
    depth_delta: float = 0.0,
) -> TreeState:
    result = await session.execute(select(TreeState).where(TreeState.user_id == user_id))
    tree = result.scalar_one_or_none()
    if tree is None:
        raise ValueError("Tree state missing")

    if depth_delta > 0:
        capped = min(depth_delta, 0.12)
        tree.growth_index = min(1.0, tree.growth_index * 0.85 + capped)

    mem_count = await session.scalar(
        select(func.count()).select_from(Memory).where(
            Memory.user_id == user_id, Memory.dismissed.is_(False)
        )
    )
    tree.leaves_count = int(mem_count or 0)

    flower_count = await session.scalar(
        select(func.count()).select_from(Memory).where(
            Memory.user_id == user_id,
            Memory.dismissed.is_(False),
            Memory.type == MemoryType.growth_event,
        )
    )
    tree.flowers_count = int(flower_count or 0)

    entry_count = await session.scalar(
        select(func.count()).select_from(JournalEntry).where(JournalEntry.user_id == user_id)
    )
    tree.branches_count = min(8, max(0, int(entry_count or 0) // 3))
    tree.roots_count = max(1, min(12, 1 + int(tree.growth_index * 10)))

    has_flower = tree.flowers_count > 0
    tree.stage = _stage_for_index(tree.growth_index, has_flower)
    await apply_season_from_activity(session, user_id, tree)
    tree.last_recomputed_at = datetime.now(timezone.utc)
    await session.flush()
    return tree


async def record_depth_signal(
    session: AsyncSession,
    user_id: UUID,
    entry_id: UUID,
    depth_score: float,
) -> float:
    magnitude = min(max(depth_score, 0.0), 1.0) * 0.08
    session.add(
        GrowthEvent(
            user_id=user_id,
            signal_type="depth",
            magnitude=magnitude,
            occurred_at=datetime.now(timezone.utc),
        )
    )
    await session.flush()
    return magnitude