import json
from typing import Any

from app.ai_guide.llm import Message, get_llm_client
from app.core.config import Settings

EXTRACT_SYSTEM = """Extract meaningful memories from the journal entry. JSON only.
Schema:
{
  "memories": [
    {
      "type": "value|belief|goal|emotional_pattern|important_moment|realization|growth_event",
      "title": "short",
      "summary": "one or two sentences",
      "confidence": 0.0
    }
  ]
}
Max 5 memories. Skip trivial restatements. confidence 0-1."""


async def extract_memories(
    body: str,
    title: str | None,
    themes: list[str],
    settings: Settings,
) -> list[dict[str, Any]]:
    llm = get_llm_client(settings.llm_provider)
    title_line = f"Title: {title}\n" if title else ""
    themes_line = f"Themes: {', '.join(themes)}\n" if themes else ""
    prompt = f"{title_line}{themes_line}Entry:\n{body}"
    raw = await llm.complete(
        [
            Message(role="system", content=EXTRACT_SYSTEM),
            Message(role="user", content=prompt),
        ],
        model=settings.llm_model_fast,
        json_mode=True,
    )
    try:
        data = json.loads(raw)
        items = data.get("memories", [])
        if isinstance(items, list):
            return items[:5]
    except json.JSONDecodeError:
        pass

    if settings.llm_provider == "stub":
        snippet = body.strip()[:80]
        return [
            {
                "type": "realization",
                "title": "Something worth keeping",
                "summary": snippet or "A moment of reflection.",
                "confidence": 0.72,
            }
        ]
    return []