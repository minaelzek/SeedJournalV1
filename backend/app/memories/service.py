from datetime import datetime
from uuid import UUID

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.db.models import Memory, MemoryType
from app.db.models_vector import MemoryEmbedding
from app.intelligence.embeddings import cosine_similarity, embed_text

MIN_CONFIDENCE = 0.55
MIN_SEARCH_SCORE_STUB = 0.35
MIN_SEARCH_SCORE = 0.72
DEDUPE_SIMILARITY = 0.92


def _parse_memory_type(value: str) -> MemoryType:
    try:
        return MemoryType(value)
    except ValueError:
        return MemoryType.realization


async def list_memories(
    session: AsyncSession,
    user_id: UUID,
    *,
    limit: int = 50,
    include_dismissed: bool = False,
) -> list[Memory]:
    q = select(Memory).where(Memory.user_id == user_id)
    if not include_dismissed:
        q = q.where(Memory.dismissed.is_(False))
    q = q.order_by(Memory.first_mentioned_at.desc()).limit(limit)
    result = await session.execute(q)
    return list(result.scalars().all())


async def dismiss_memory(session: AsyncSession, user_id: UUID, memory_id: UUID) -> Memory | None:
    result = await session.execute(
        select(Memory).where(Memory.id == memory_id, Memory.user_id == user_id)
    )
    memory = result.scalar_one_or_none()
    if memory is None:
        return None
    memory.dismissed = True
    await session.flush()
    return memory


async def _is_duplicate(
    session: AsyncSession,
    user_id: UUID,
    embedding: list[float],
) -> bool:
    result = await session.execute(
        select(MemoryEmbedding)
        .join(Memory, Memory.id == MemoryEmbedding.memory_id)
        .where(Memory.user_id == user_id, Memory.dismissed.is_(False))
        .limit(50)
    )
    for row in result.scalars().all():
        if cosine_similarity(row.embedding, embedding) >= DEDUPE_SIMILARITY:
            return True
    return False


async def create_memory_with_embedding(
    session: AsyncSession,
    *,
    user_id: UUID,
    source_entry_id: UUID,
    first_mentioned_at: datetime,
    item: dict,
    settings: Settings,
) -> Memory | None:
    confidence = float(item.get("confidence", 0))
    if confidence < MIN_CONFIDENCE:
        return None

    summary = str(item.get("summary", "")).strip()
    title = str(item.get("title", "Reflection")).strip() or "Reflection"
    if not summary:
        return None

    embed_input = f"{title}\n{summary}"
    embedding = await embed_text(embed_input, settings)
    if await _is_duplicate(session, user_id, embedding):
        return None

    memory = Memory(
        user_id=user_id,
        source_entry_id=source_entry_id,
        type=_parse_memory_type(str(item.get("type", "realization"))),
        title=title[:512],
        summary=summary,
        confidence=confidence,
        first_mentioned_at=first_mentioned_at,
    )
    session.add(memory)
    await session.flush()

    session.add(
        MemoryEmbedding(
            memory_id=memory.id,
            embedding=embedding,
            model=settings.embedding_model,
        )
    )
    await session.flush()
    return memory


async def _search_memories_python(
    session: AsyncSession,
    user_id: UUID,
    q_emb: list[float],
    min_score: float,
    limit: int,
) -> list[tuple[Memory, float]]:
    result = await session.execute(
        select(Memory, MemoryEmbedding)
        .join(MemoryEmbedding, MemoryEmbedding.memory_id == Memory.id)
        .where(Memory.user_id == user_id, Memory.dismissed.is_(False))
    )
    scored: list[tuple[Memory, float]] = []
    for memory, emb_row in result.all():
        vec = list(emb_row.embedding)
        score = cosine_similarity(q_emb, vec)
        if score >= min_score:
            scored.append((memory, score))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:limit]


async def search_memories(
    session: AsyncSession,
    user_id: UUID,
    query: str,
    settings: Settings,
    *,
    limit: int = 10,
) -> list[tuple[Memory, float]]:
    query = query.strip()
    if not query:
        return []

    q_emb = await embed_text(query, settings)
    min_score = MIN_SEARCH_SCORE_STUB if settings.llm_provider == "stub" else MIN_SEARCH_SCORE

    if settings.llm_provider == "stub":
        return await _search_memories_python(session, user_id, q_emb, min_score, limit)

    sql = text(
        """
        SELECT m.id,
               1 - (e.embedding <=> CAST(:qvec AS vector)) AS score
        FROM memories m
        JOIN memory_embeddings e ON e.memory_id = m.id
        WHERE m.user_id = :uid
          AND m.dismissed = false
          AND (1 - (e.embedding <=> CAST(:qvec AS vector))) >= :min_score
        ORDER BY e.embedding <=> CAST(:qvec AS vector)
        LIMIT :lim
        """
    )
    vec_literal = "[" + ",".join(str(x) for x in q_emb) + "]"
    try:
        rows = await session.execute(
            sql,
            {"qvec": vec_literal, "uid": str(user_id), "min_score": min_score, "lim": limit},
        )
        ids_scores = [(UUID(row[0]), float(row[1])) for row in rows.fetchall()]
    except Exception:
        return await _search_memories_python(session, user_id, q_emb, min_score, limit)

    if not ids_scores:
        return []

    ids = [i for i, _ in ids_scores]
    result = await session.execute(select(Memory).where(Memory.id.in_(ids)))
    by_id = {m.id: m for m in result.scalars().all()}
    return [(by_id[i], s) for i, s in ids_scores if i in by_id]