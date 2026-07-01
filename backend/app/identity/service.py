from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import TreeStage, Season, TreeState, User


async def get_user_by_id(session: AsyncSession, user_id: UUID) -> User | None:
    result = await session.execute(
        select(User).where(User.id == user_id, User.deleted_at.is_(None))
    )
    return result.scalar_one_or_none()


async def get_or_create_user_from_apple(
    session: AsyncSession,
    *,
    apple_sub: str,
    email: str | None,
) -> User:
    result = await session.execute(
        select(User).where(User.apple_sub == apple_sub, User.deleted_at.is_(None))
    )
    user = result.scalar_one_or_none()
    if user:
        if email and user.email != email:
            user.email = email
        return user

    user = User(apple_sub=apple_sub, email=email)
    session.add(user)
    await session.flush()

    tree = TreeState(
        user_id=user.id,
        stage=TreeStage.seed,
        season=Season.spring,
        growth_index=0.0,
        roots_count=1,
        branches_count=0,
        leaves_count=0,
        flowers_count=0,
    )
    session.add(tree)
    await session.flush()
    return user