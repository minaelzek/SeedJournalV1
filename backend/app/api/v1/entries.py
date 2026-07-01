from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth_deps import get_current_user_id
from app.core.deps import get_db
from app.core.idempotency import get_cached_response, store_cached_response
from app.journal.service import create_entry, get_entry_for_user, list_entries_for_user

router = APIRouter()


class EntryCreate(BaseModel):
    title: str | None = None
    body: str = Field(min_length=1)


class EntryResponse(BaseModel):
    id: UUID
    title: str | None
    body: str
    word_count: int
    reflection_completed: bool
    created_at: datetime


class EntryListItem(BaseModel):
    id: UUID
    title: str | None
    body_preview: str
    word_count: int
    reflection_completed: bool
    created_at: datetime


class EntryListResponse(BaseModel):
    items: list[EntryListItem]
    next_cursor: datetime | None


def _to_response(entry) -> EntryResponse:
    return EntryResponse(
        id=entry.id,
        title=entry.title,
        body=entry.body,
        word_count=entry.word_count,
        reflection_completed=entry.reflection_completed,
        created_at=entry.created_at,
    )


@router.post("", response_model=EntryResponse, status_code=status.HTTP_201_CREATED)
async def create_journal_entry(
    payload: EntryCreate,
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
) -> EntryResponse:
    if idempotency_key:
        cache_key = f"entry:{user_id}:{idempotency_key}"
        cached = get_cached_response(cache_key)
        if cached:
            return EntryResponse.model_validate_json(cached)
    entry = await create_entry(
        session,
        user_id=user_id,
        title=payload.title,
        body=payload.body,
    )
    await session.commit()
    response = _to_response(entry)
    if idempotency_key:
        store_cached_response(f"entry:{user_id}:{idempotency_key}", response.model_dump_json())
    return response


@router.get("", response_model=EntryListResponse)
async def list_journal_entries(
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db),
    limit: int = Query(default=20, ge=1, le=50),
    cursor: datetime | None = Query(default=None),
) -> EntryListResponse:
    entries = await list_entries_for_user(session, user_id, limit=limit, before=cursor)
    items = [
        EntryListItem(
            id=e.id,
            title=e.title,
            body_preview=(e.body[:120] + "...") if len(e.body) > 120 else e.body,
            word_count=e.word_count,
            reflection_completed=e.reflection_completed,
            created_at=e.created_at,
        )
        for e in entries
    ]
    next_cursor = entries[-1].created_at if len(entries) == limit else None
    return EntryListResponse(items=items, next_cursor=next_cursor)


@router.get("/{entry_id}", response_model=EntryResponse)
async def get_journal_entry(
    entry_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db),
) -> EntryResponse:
    entry = await get_entry_for_user(session, user_id, entry_id)
    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
    return _to_response(entry)