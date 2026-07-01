from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.auth_deps import get_current_user
from app.db.models import User

router = APIRouter()


class MeResponse(BaseModel):
    id: UUID
    email: str | None
    timezone: str
    ai_depth_enabled: bool
    created_at: datetime


@router.get("/me", response_model=MeResponse)
async def get_me(user: User = Depends(get_current_user)) -> MeResponse:
    return MeResponse(
        id=user.id,
        email=user.email,
        timezone=user.timezone,
        ai_depth_enabled=user.ai_depth_enabled,
        created_at=user.created_at,
    )