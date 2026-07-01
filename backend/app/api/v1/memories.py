from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth_deps import get_current_user_id
from app.core.config import Settings, get_settings
from app.core.deps import get_db
from app.memories.service import dismiss_memory, list_memories, search_memories

router = APIRouter()


class MemoryItem(BaseModel):
    id: UUID
    type: str
    title: str
    summary: str
    confidence: float
    dismissed: bool
    source_entry_id: UUID
    first_mentioned_at: datetime
    created_at: datetime
    score: float | None = None


class MemoryListResponse(BaseModel):
    items: list[MemoryItem]


class MemorySearchRequest(BaseModel):
    query: str = Field(min_length=1)
    limit: int = Field(default=10, ge=1, le=30)


class MemoryPatch(BaseModel):
    dismissed: bool | None = None


def _to_item(memory, score: float | None = None) -> MemoryItem:
    return MemoryItem(
        id=memory.id,
        type=memory.type.value,
        title=memory.title,
        summary=memory.summary,
        confidence=memory.confidence,
        dismissed=memory.dismissed,
        source_entry_id=memory.source_entry_id,
        first_mentioned_at=memory.first_mentioned_at,
        created_at=memory.created_at,
        score=score,
    )


@router.get("", response_model=MemoryListResponse)
async def get_memories(
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db),
    limit: int = Query(default=50, ge=1, le=100),
) -> MemoryListResponse:
    rows = await list_memories(session, user_id, limit=limit)
    return MemoryListResponse(items=[_to_item(m) for m in rows])


@router.post("/search", response_model=MemoryListResponse)
async def post_memory_search(
    body: MemorySearchRequest,
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> MemoryListResponse:
    results = await search_memories(session, user_id, body.query, settings, limit=body.limit)
    return MemoryListResponse(items=[_to_item(m, score=s) for m, s in results])


@router.patch("/{memory_id}", response_model=MemoryItem)
async def patch_memory(
    memory_id: UUID,
    body: MemoryPatch,
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db),
) -> MemoryItem:
    if body.dismissed is True:
        memory = await dismiss_memory(session, user_id, memory_id)
        if memory is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memory not found")
        await session.commit()
        return _to_item(memory)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No supported changes")