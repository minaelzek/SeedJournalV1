import hashlib
import math

from app.core.config import Settings
from app.db.models_vector import EMBEDDING_DIM

_stub_cache: dict[str, list[float]] = {}


def _stub_embedding(text: str) -> list[float]:
    if text in _stub_cache:
        return _stub_cache[text]
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    vec = []
    for i in range(EMBEDDING_DIM):
        byte = digest[i % len(digest)]
        seed = (byte + i * 17) % 256
        vec.append((seed / 127.5) - 1.0)
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    vec = [x / norm for x in vec]
    _stub_cache[text] = vec
    return vec


async def embed_text(text: str, settings: Settings) -> list[float]:
    if settings.llm_provider == "stub":
        return _stub_embedding(text.strip())
    if settings.llm_provider == "openai":
        from app.ai_guide.openai_client import openai_embed

        vec = await openai_embed(text, settings)
        if len(vec) != EMBEDDING_DIM:
            raise ValueError(f"Expected {EMBEDDING_DIM} dimensions, got {len(vec)}")
        return vec
    raise NotImplementedError("Embedding provider not configured for this LLM_PROVIDER")


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b, strict=False))
    na = math.sqrt(sum(x * x for x in a)) or 1.0
    nb = math.sqrt(sum(x * x for x in b)) or 1.0
    return dot / (na * nb)