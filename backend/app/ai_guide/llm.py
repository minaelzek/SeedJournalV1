"""Pluggable LLM client — stub for local dev without API keys."""

from dataclasses import dataclass
from typing import Protocol


@dataclass
class Message:
    role: str
    content: str


class LLMClient(Protocol):
    async def complete(
        self,
        messages: list[Message],
        *,
        model: str,
        json_mode: bool = False,
    ) -> str: ...


class StubLLMClient:
    async def complete(
        self,
        messages: list[Message],
        *,
        model: str,
        json_mode: bool = False,
    ) -> str:
        if json_mode:
            system = messages[0].content if messages else ""
            if "memories" in system.lower() or "extract" in system.lower():
                return (
                    '{"memories":[{"type":"realization",'
                    '"title":"A thread to keep","summary":"Something in this entry feels worth returning to.",'
                    '"confidence":0.78}]}'
                )
            return (
                '{"themes":["reflection"],'
                '"depth_score":0.4,'
                '"emotional_tone":"neutral",'
                '"sensitivity_flags":["none"]}'
            )
        last = messages[-1].content if messages else ""
        return (
            "Thank you for sharing that. "
            "What feels most true for you in this moment?"
        )


def get_llm_client(provider: str) -> LLMClient:
    if provider == "stub":
        return StubLLMClient()
    if provider == "openai":
        from app.core.config import get_settings
        from app.ai_guide.openai_client import OpenAILLMClient

        return OpenAILLMClient(get_settings())
    raise NotImplementedError(f"LLM provider not configured: {provider}")