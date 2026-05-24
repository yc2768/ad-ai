import base64
import json
import logging
from collections.abc import AsyncIterator
from typing import Any

import httpx

from app.core.config import Settings, settings

logger = logging.getLogger(__name__)


class SeedreamService:
    """火山方舟 Seedream 图片生成（/api/v3/images/generations），供业务 Service 内部调用。"""

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
        return model or self._cfg.ark_image_model

    async def resolve_image_refs(self, refs: list[str]) -> list[str]:
        """将 HTTP 参考图转为 data URI，避免方舟侧拉取外链 403。"""
        resolved: list[str] = []
        for ref in refs:
            if ref.startswith(("http://", "https://")):
                resolved.append(await self._download_as_data_uri(ref))
            else:
                resolved.append(ref)
        return resolved

    async def _download_as_data_uri(self, url: str) -> str:
        try:
            async with httpx.AsyncClient(
                timeout=60.0,
                follow_redirects=True,
                headers={"User-Agent": "Mozilla/5.0 (compatible; ad-ai/1.0)"},
            ) as client:
                response = await client.get(url)
                response.raise_for_status()
        except httpx.HTTPError as exc:
            raise ValueError(f"无法下载参考图，请检查 URL 是否可访问: {url}") from exc
        content_type = (
            response.headers.get("content-type", "image/jpeg").split(";")[0].strip()
            or "image/jpeg"
        )
        encoded = base64.standard_b64encode(response.content).decode("ascii")
        logger.debug("seedream image fetched | url=%s bytes=%d", url[:80], len(response.content))
        return f"data:{content_type};base64,{encoded}"

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

    async def generate(self, payload: dict[str, Any]) -> dict[str, Any]:
        """非流式图片生成。"""
        self._ensure_configured()
        body = {**payload, "stream": False}
        logger.debug("seedream generate | model=%s", body.get("model"))
        response = await self._client.post("/api/v3/images/generations", json=body)
        if response.is_error:
            raise ValueError(self._parse_error(response))
        return response.json()

    async def generate_stream(self, payload: dict[str, Any]) -> AsyncIterator[dict[str, Any]]:
        """流式图片生成（SSE）。"""
        self._ensure_configured()
        body = {**payload, "stream": True}
        logger.debug("seedream stream | model=%s", body.get("model"))

        async with self._client.stream(
            "POST",
            "/api/v3/images/generations",
            json=body,
        ) as response:
            if response.is_error:
                body = await response.aread()
                raise ValueError(
                    self._parse_error(
                        httpx.Response(response.status_code, content=body)
                    )
                )
            async for event in self._iter_sse_events(response):
                yield event

    @staticmethod
    async def _iter_sse_events(response: httpx.Response) -> AsyncIterator[dict[str, Any]]:
        async for line in response.aiter_lines():
            if not line or not line.startswith("data:"):
                continue
            raw = line[5:].strip()
            if raw == "[DONE]":
                break
            try:
                yield json.loads(raw)
            except json.JSONDecodeError:
                logger.warning("seedream stream skip invalid json: %s", raw[:120])

    async def aclose(self) -> None:
        await self._client.aclose()
