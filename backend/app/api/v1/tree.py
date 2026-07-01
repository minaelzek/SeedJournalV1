from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth_deps import get_current_user_id
from app.core.deps import get_db
from app.db.models import TreeState
from uuid import UUID

router = APIRouter()


class TreeStateResponse(BaseModel):
    stage: str
    season: str
    roots_count: int
    branches_count: int
    leaves_count: int
    flowers_count: int


@router.get("", response_model=TreeStateResponse)
async def get_tree(
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db),
) -> TreeStateResponse:
    result = await session.execute(select(TreeState).where(TreeState.user_id == user_id))
    tree = result.scalar_one_or_none()
    if tree is None:
        return TreeStateResponse(
            stage="seed",
            season="spring",
            roots_count=1,
            branches_count=0,
            leaves_count=0,
            flowers_count=0,
        )
    return TreeStateResponse(
        stage=tree.stage.value,
        season=tree.season.value,
        roots_count=tree.roots_count,
        branches_count=tree.branches_count,
        leaves_count=tree.leaves_count,
        flowers_count=tree.flowers_count,
    )