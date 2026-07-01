from collections import Counter
from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth_deps import get_current_user_id
from app.core.config import Settings, get_settings
from app.core.deps import get_db
from app.db.models import Memory
from app.memories.service import search_memories

router = APIRouter()


class PatternItem(BaseModel):
    memory_type: str
    count: int


class PatternsResponse(BaseModel):
    items: list[PatternItem]
    narrative: str


class FirstMentionItem(BaseModel):
    memory_id: UUID
    title: str
    summary: str
    first_mentioned_at: datetime
    score: float


class FirstMentionResponse(BaseModel):
    query: str
    items: list[FirstMentionItem]
    narrative: str


@router.get("/patterns", response_model=PatternsResponse)
async def get_patterns(
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db),
) -> PatternsResponse:
    result = await session.execute(
        select(Memory.type, Memory.id)
        .where(Memory.user_id == user_id, Memory.dismissed.is_(False))
    )
    counter: Counter[str] = Counter()
    for mem_type, _ in result.all():
        counter[mem_type.value] += 1

    items = [PatternItem(memory_type=k, count=v) for k, v in counter.most_common(6)]
    if not items:
        narrative = "Your meaningful memories will gather quietly as you reflect."
    else:
        top = items[0]
        narrative = (
            f"You've named several {top.memory_type.replace('_', ' ')} themes in your journal. "
            "These are patterns you've noticed — not labels."
        )
    return PatternsResponse(items=items, narrative=narrative)


@router.get("/first-mention", response_model=FirstMentionResponse)
async def get_first_mention(
    q: str = Query(min_length=1),
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> FirstMentionResponse:
    results = await search_memories(session, user_id, q, settings, limit=5)
    items = [
        FirstMentionItem(
            memory_id=m.id,
            title=m.title,
            summary=m.summary,
            first_mentioned_at=m.first_mentioned_at,
            score=s,
        )
        for m, s in results
    ]
    items.sort(key=lambda x: x.first_mentioned_at)
    if items:
        first = items[0]
        narrative = (
            f"The earliest related memory in your journal appears around "
            f"{first.first_mentioned_at.date().isoformat()}."
        )
    else:
        narrative = "Nothing close enough yet — keep writing; meaning accumulates over time."
    return FirstMentionResponse(query=q, items=items, narrative=narrative)