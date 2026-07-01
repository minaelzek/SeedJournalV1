import json

from app.ai_guide.llm import Message, get_llm_client
from app.core.config import Settings

ANALYSIS_SYSTEM = """Analyze the journal entry and respond with JSON only.
Schema:
{
  "themes": ["string"],
  "depth_score": 0.0,
  "emotional_tone": "neutral",
  "sensitivity_flags": ["none"]
}
depth_score is 0-1 based on self-reflection depth. sensitivity_flags may include crisis_language or none."""


async def analyze_entry(body: str, title: str | None, settings: Settings) -> dict:
    llm = get_llm_client(settings.llm_provider)
    title_line = f"Title: {title}\n" if title else ""
    prompt = f"{title_line}{body}"
    raw = await llm.complete(
        [
            Message(role="system", content=ANALYSIS_SYSTEM),
            Message(role="user", content=prompt),
        ],
        model=settings.llm_model_fast,
        json_mode=True,
    )
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = {
            "themes": ["reflection"],
            "depth_score": 0.35,
            "emotional_tone": "neutral",
            "sensitivity_flags": ["none"],
        }
    depth = float(data.get("depth_score", 0.35))
    data["depth_score"] = max(0.0, min(1.0, depth))
    if "themes" not in data:
        data["themes"] = []
    return data