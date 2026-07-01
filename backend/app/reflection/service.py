from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.ai_guide.llm import Message, get_llm_client
from app.ai_guide.prompts import GUIDE_SYSTEM_PROMPT, build_entry_context
from app.core.config import Settings
from app.db.models import JournalEntry, ReflectionRole, ReflectionSession, ReflectionTurn

MAX_TURNS = 6


class ReflectionError(Exception):
    pass


async def get_session_for_entry(
    session: AsyncSession, user_id: UUID, entry_id: UUID
) -> ReflectionSession | None:
    result = await session.execute(
        select(ReflectionSession)
        .where(ReflectionSession.entry_id == entry_id, ReflectionSession.user_id == user_id)
        .options(selectinload(ReflectionSession.turns))
    )
    return result.scalar_one_or_none()


async def _get_entry(session: AsyncSession, user_id: UUID, entry_id: UUID) -> JournalEntry:
    result = await session.execute(
        select(JournalEntry).where(
            JournalEntry.id == entry_id,
            JournalEntry.user_id == user_id,
        )
    )
    entry = result.scalar_one_or_none()
    if entry is None:
        raise ReflectionError("Entry not found")
    return entry


def _turns_ordered(turns: list[ReflectionTurn]) -> list[ReflectionTurn]:
    return sorted(turns, key=lambda t: t.sequence)


async def _generate_assistant_reply(
    *,
    settings: Settings,
    entry: JournalEntry,
    turns: list[ReflectionTurn],
) -> str:
    llm = get_llm_client(settings.llm_provider)
    messages = [Message(role="system", content=GUIDE_SYSTEM_PROMPT)]
    messages.append(
        Message(
            role="user",
            content=build_entry_context(entry.title, entry.body)
            + "\n\n(The user saved this reflection. Begin with one gentle follow-up question.)",
        )
    )
    for turn in _turns_ordered(turns):
        role = "assistant" if turn.role == ReflectionRole.assistant else "user"
        messages.append(Message(role=role, content=turn.content))

    return await llm.complete(messages, model=settings.llm_model_guide, json_mode=False)


async def start_reflection(
    db: AsyncSession,
    *,
    user_id: UUID,
    entry_id: UUID,
    settings: Settings,
    ai_enabled: bool,
) -> tuple[ReflectionSession, ReflectionTurn | None]:
    entry = await _get_entry(db, user_id, entry_id)
    existing = await get_session_for_entry(db, user_id, entry_id)
    if existing is not None:
        if existing.completed_at is not None:
            raise ReflectionError("Reflection already completed")
        turns = _turns_ordered(list(existing.turns))
        if turns:
            last_assistant = next(
                (t for t in reversed(turns) if t.role == ReflectionRole.assistant),
                None,
            )
            return existing, last_assistant
        reflection = existing
    else:
        reflection = ReflectionSession(entry_id=entry_id, user_id=user_id, turn_count=0)
        db.add(reflection)
        await db.flush()

    if not ai_enabled:
        return reflection, None

    content = await _generate_assistant_reply(settings=settings, entry=entry, turns=[])
    assistant_turn = ReflectionTurn(
        session_id=reflection.id,
        role=ReflectionRole.assistant,
        content=content,
        sequence=0,
    )
    db.add(assistant_turn)
    reflection.turn_count = 1
    await db.flush()
    await db.refresh(reflection)
    return reflection, assistant_turn


async def add_user_turn_and_reply(
    db: AsyncSession,
    *,
    user_id: UUID,
    entry_id: UUID,
    user_message: str,
    settings: Settings,
) -> tuple[ReflectionTurn, ReflectionTurn | None]:
    entry = await _get_entry(db, user_id, entry_id)
    reflection = await get_session_for_entry(db, user_id, entry_id)
    if reflection is None or reflection.completed_at is not None:
        raise ReflectionError("No active reflection session")

    if reflection.turn_count >= MAX_TURNS:
        raise ReflectionError("Turn limit reached")

    text = user_message.strip()
    if not text:
        raise ReflectionError("Message cannot be empty")

    next_seq = reflection.turn_count
    user_turn = ReflectionTurn(
        session_id=reflection.id,
        role=ReflectionRole.user,
        content=text,
        sequence=next_seq,
    )
    db.add(user_turn)
    reflection.turn_count += 1

    if reflection.turn_count >= MAX_TURNS:
        await db.flush()
        return user_turn, None

    turns = _turns_ordered(list(reflection.turns) + [user_turn])
    assistant_content = await _generate_assistant_reply(
        settings=settings, entry=entry, turns=turns
    )
    assistant_turn = ReflectionTurn(
        session_id=reflection.id,
        role=ReflectionRole.assistant,
        content=assistant_content,
        sequence=reflection.turn_count,
    )
    db.add(assistant_turn)
    reflection.turn_count += 1
    await db.flush()
    return user_turn, assistant_turn


async def complete_reflection(
    db: AsyncSession,
    *,
    user_id: UUID,
    entry_id: UUID,
) -> ReflectionSession:
    entry = await _get_entry(db, user_id, entry_id)
    reflection = await get_session_for_entry(db, user_id, entry_id)
    if reflection is None:
        reflection = ReflectionSession(entry_id=entry_id, user_id=user_id, turn_count=0)
        db.add(reflection)
        await db.flush()

    reflection.completed_at = datetime.now(timezone.utc)
    entry.reflection_completed = True
    await db.flush()
    await db.refresh(reflection)
    return reflection