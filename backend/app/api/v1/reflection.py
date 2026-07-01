import os
from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth_deps import get_current_user
from app.core.config import Settings, get_settings
from app.core.deps import get_db
from app.db.models import User
from app.journal.service import get_entry_for_user
from app.workers.tasks import enqueue_entry_pipeline
from app.reflection.service import (
    ReflectionError,
    add_user_turn_and_reply,
    complete_reflection,
    get_session_for_entry,
    start_reflection,
)

router = APIRouter()


class ReflectionTurnDTO(BaseModel):
    id: UUID
    role: str
    content: str
    sequence: int
    created_at: datetime


class ReflectionStateResponse(BaseModel):
    entry_id: UUID
    session_id: UUID | None
    completed: bool
    turn_count: int
    max_turns: int
    turns: list[ReflectionTurnDTO]


class ReflectionStartResponse(BaseModel):
    session_id: UUID
    assistant_message: ReflectionTurnDTO | None
    turn_count: int
    max_turns: int


class ReflectionMessageRequest(BaseModel):
    message: str = Field(min_length=1)


class ReflectionMessageResponse(BaseModel):
    user_turn: ReflectionTurnDTO
    assistant_turn: ReflectionTurnDTO | None
    turn_count: int
    max_turns: int
    limit_reached: bool


class ReflectionCompleteResponse(BaseModel):
    entry_id: UUID
    reflection_completed: bool
    completed_at: datetime | None


def _turn_dto(turn) -> ReflectionTurnDTO:
    return ReflectionTurnDTO(
        id=turn.id,
        role=turn.role.value,
        content=turn.content,
        sequence=turn.sequence,
        created_at=turn.created_at,
    )


@router.get("/{entry_id}/reflection", response_model=ReflectionStateResponse)
async def get_reflection_state(
    entry_id: UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> ReflectionStateResponse:
    entry = await get_entry_for_user(session, user.id, entry_id)
    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")

    reflection = await get_session_for_entry(session, user.id, entry_id)
    if reflection is None:
        return ReflectionStateResponse(
            entry_id=entry_id,
            session_id=None,
            completed=entry.reflection_completed,
            turn_count=0,
            max_turns=6,
            turns=[],
        )

    turns = sorted(reflection.turns, key=lambda t: t.sequence)
    return ReflectionStateResponse(
        entry_id=entry_id,
        session_id=reflection.id,
        completed=reflection.completed_at is not None or entry.reflection_completed,
        turn_count=reflection.turn_count,
        max_turns=6,
        turns=[_turn_dto(t) for t in turns],
    )


@router.post("/{entry_id}/reflection/start", response_model=ReflectionStartResponse)
async def start_entry_reflection(
    entry_id: UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> ReflectionStartResponse:
    try:
        reflection, assistant = await start_reflection(
            session,
            user_id=user.id,
            entry_id=entry_id,
            settings=settings,
            ai_enabled=user.ai_depth_enabled,
        )
        await session.commit()
    except ReflectionError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return ReflectionStartResponse(
        session_id=reflection.id,
        assistant_message=_turn_dto(assistant) if assistant else None,
        turn_count=reflection.turn_count,
        max_turns=6,
    )


@router.post("/{entry_id}/reflection/message", response_model=ReflectionMessageResponse)
async def post_reflection_message(
    entry_id: UUID,
    body: ReflectionMessageRequest,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> ReflectionMessageResponse:
    if not user.ai_depth_enabled:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="AI depth is disabled")

    try:
        user_turn, assistant_turn = await add_user_turn_and_reply(
            session,
            user_id=user.id,
            entry_id=entry_id,
            user_message=body.message,
            settings=settings,
        )
        reflection = await get_session_for_entry(session, user.id, entry_id)
        await session.commit()
    except ReflectionError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    assert reflection is not None
    limit_reached = reflection.turn_count >= 6 or assistant_turn is None
    return ReflectionMessageResponse(
        user_turn=_turn_dto(user_turn),
        assistant_turn=_turn_dto(assistant_turn) if assistant_turn else None,
        turn_count=reflection.turn_count,
        max_turns=6,
        limit_reached=limit_reached,
    )


@router.post("/{entry_id}/reflection/complete", response_model=ReflectionCompleteResponse)
async def complete_entry_reflection(
    entry_id: UUID,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> ReflectionCompleteResponse:
    try:
        reflection = await complete_reflection(session, user_id=user.id, entry_id=entry_id)
        await session.commit()
    except ReflectionError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    # TestClient / CI: run pipeline inline so memory/tree tests are reliable
    if os.getenv("PYTEST_CURRENT_TEST"):
        await enqueue_entry_pipeline(user.id, entry_id)
    else:
        background_tasks.add_task(enqueue_entry_pipeline, user.id, entry_id)

    return ReflectionCompleteResponse(
        entry_id=entry_id,
        reflection_completed=True,
        completed_at=reflection.completed_at,
    )