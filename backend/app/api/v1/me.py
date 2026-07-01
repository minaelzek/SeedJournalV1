from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth_deps import get_current_user
from app.core.deps import get_db
from app.db.models import User
from app.identity.service import update_user_preferences

router = APIRouter()


class MeResponse(BaseModel):
    id: UUID
    email: str | None
    timezone: str
    ai_depth_enabled: bool
    created_at: datetime


class MePatchRequest(BaseModel):
    timezone: str | None = Field(default=None, max_length=64)
    ai_depth_enabled: bool | None = None


@router.get("/me", response_model=MeResponse)
async def get_me(user: User = Depends(get_current_user)) -> MeResponse:
    return MeResponse(
        id=user.id,
        email=user.email,
        timezone=user.timezone,
        ai_depth_enabled=user.ai_depth_enabled,
        created_at=user.created_at,
    )


@router.patch("/me", response_model=MeResponse)
async def patch_me(
    payload: MePatchRequest,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> MeResponse:
    updated = await update_user_preferences(
        session,
        user.id,
        timezone=payload.timezone,
        ai_depth_enabled=payload.ai_depth_enabled,
    )
    await session.commit()
    u = updated or user
    return MeResponse(
        id=u.id,
        email=u.email,
        timezone=u.timezone,
        ai_depth_enabled=u.ai_depth_enabled,
        created_at=u.created_at,
    )