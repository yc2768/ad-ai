import json
import logging
from typing import Any

import httpx

from app.core.config import Settings, settings

logger = logging.getLogger(__name__)

class SeedanceService:
    """火山方舟 Seedance 视频生成（/api/v3/contents/generations/tasks）。"""

    def __init__(self, cfg: Settings = settings) -> None:
        self._cfg = cfg
        self._client = httpx.AsyncClient(
            base_url=cfg.ark_base_url.rstrip("/"),
            headers={
                "Authorization": f"Bearer {cfg.ark_api_key or ''}",
                "Content-Type": "application/json",
            },
            timeout=300.0,
        )

    def _ensure_configured(self) -> None:
        if not self._cfg.ark_api_key:
            raise ValueError("ARK_API_KEY 未配置，请在 .env 中设置")

    def resolve_model(self, model: str | None = None) -> str:
        return model or self._cfg.ark_video_model

    @staticmethod
    def _parse_error(response: httpx.Response) -> str:
        try:
            body = response.json()
            if isinstance(body, dict):
                err = body.get("error")
                if isinstance(err, dict) and err.get("message"):
                    return str(err["message"])
        except json.JSONDecodeError:
            pass
        return response.text or f"HTTP {response.status_code}"

    async def create_task(self, payload: dict[str, Any]) -> dict[str, Any]:
        self._ensure_configured()
        logger.debug("seedance create | model=%s", payload.get("model"))
        response = await self._client.post(
            "/api/v3/contents/generations/tasks",
            json=payload,
        )
        if response.is_error:
            raise ValueError(self._parse_error(response))
        return response.json()

    async def get_task(self, task_id: str) -> dict[str, Any]:
        self._ensure_configured()
        response = await self._client.get(
            f"/api/v3/contents/generations/tasks/{task_id}",
        )
        if response.is_error:
            raise ValueError(self._parse_error(response))
        return response.json()

    @staticmethod
    def extract_video_url(task: dict[str, Any]) -> str:
        content = task.get("content")
        if isinstance(content, dict):
            url = content.get("video_url")
            if url:
                return str(url)
        output = task.get("output")
        if isinstance(output, dict):
            for key in ("video_url", "url"):
                if output.get(key):
                    return str(output[key])
        return ""

    async def aclose(self) -> None:
        await self._client.aclose()
