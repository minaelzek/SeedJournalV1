import httpx

from app.ai_guide.llm import Message
from app.core.config import Settings


class OpenAILLMClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._api_key = settings.openai_api_key

    async def complete(
        self,
        messages: list[Message],
        *,
        model: str,
        json_mode: bool = False,
    ) -> str:
        payload: dict = {
            "model": model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        async with httpx.AsyncClient(timeout=self._settings.llm_timeout_sec) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]


async def openai_embed(text: str, settings: Settings) -> list[float]:
    async with httpx.AsyncClient(timeout=self._settings.llm_timeout_sec) as client:
        response = await client.post(
            "https://api.openai.com/v1/embeddings",
            headers={
                "Authorization": f"Bearer {settings.openai_api_key}",
                "Content-Type": "application/json",
            },
            json={"model": settings.embedding_model, "input": text.strip()},
        )
        response.raise_for_status()
        data = response.json()
        return data["data"][0]["embedding"]