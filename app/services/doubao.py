import logging
from typing import Any

import httpx
from langchain_core.messages import BaseMessage

from app.core.config import Settings, settings

logger = logging.getLogger(__name__)


class DoubaoService:
    """豆包（火山方舟）基础能力，仅供业务 Service 内部调用。"""

    def __init__(self, cfg: Settings = settings) -> None:
        self._cfg = cfg
        self._client = httpx.AsyncClient(
            base_url=cfg.ark_base_url.rstrip("/"),
            headers={
                "Authorization": f"Bearer {cfg.ark_api_key or ''}",
                "Content-Type": "application/json",
            },
            timeout=120.0,
        )

    def _ensure_configured(self) -> None:
        if not self._cfg.ark_api_key:
            raise ValueError("ARK_API_KEY 未配置，请在 .env 中设置")

    def resolve_model(self, model: str | None = None) -> str:
        return model or self._cfg.ark_default_model

    @staticmethod
    def messages_to_input(messages: list[BaseMessage]) -> list[dict[str, Any]]:
        role_map = {"human": "user", "ai": "assistant", "system": "system"}
        result: list[dict[str, Any]] = []
        for msg in messages:
            role = role_map.get(msg.type, "user")
            result.append(
                {
                    "role": role,
                    "content": [{"type": "input_text", "text": msg.content}],
                }
            )
        return result

    async def invoke(
        self,
        messages: list[BaseMessage],
        model: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        self._ensure_configured()
        model_id = self.resolve_model(model)
        payload: dict[str, Any] = {
            "model": model_id,
            "input": self.messages_to_input(messages),
            **extra,
        }
        logger.debug("doubao invoke | model=%s", model_id)
        response = await self._client.post("/api/v3/responses", json=payload)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def extract_text(response: dict[str, Any]) -> str:
        """从 Ark Responses 结果中提取文本。"""
        output = response.get("output")
        if isinstance(output, list):
            parts: list[str] = []
            for item in output:
                if not isinstance(item, dict):
                    continue
                content = item.get("content")
                if isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get("text"):
                            parts.append(str(block["text"]))
                elif item.get("text"):
                    parts.append(str(item["text"]))
            if parts:
                return "\n".join(parts)
        if isinstance(output, dict) and output.get("text"):
            return str(output["text"])
        choices = response.get("choices")
        if isinstance(choices, list) and choices:
            message = choices[0].get("message", {})
            if message.get("content"):
                return str(message["content"])
        return str(response)

    async def aclose(self) -> None:
        await self._client.aclose()
