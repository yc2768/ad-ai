import logging
from collections.abc import AsyncIterator
from typing import Any

from app.schemas.ad_image import (
    AdImageItem,
    AdImageMode,
    AdImageRequest,
    AdImageResponse,
)
from app.services.seedream import SeedreamService

logger = logging.getLogger(__name__)


class AdImageService:
    """广告图片提效：按模式组装 Seedream 5.0 lite 请求。"""

    def __init__(self, seedream: SeedreamService) -> None:
        self._seedream = seedream

    def build_payload(
        self,
        request: AdImageRequest,
        *,
        images: list[str] | None = None,
    ) -> dict[str, Any]:
        model = self._seedream.resolve_model(request.model)
        refs = images if images is not None else request.images

        payload: dict[str, Any] = {
            "model": model,
            "prompt": request.prompt,
            "size": request.size,
            "response_format": "url",
            "watermark": request.watermark,
            "sequential_image_generation": "disabled",
        }

        if request.web_search:
            payload["enable_online_search"] = True
            payload["model"] = self._seedream.resolve_model(None)

        if refs:
            payload["image"] = refs[0] if len(refs) == 1 else refs

        if request.mode == AdImageMode.MULTI_REFERENCE_GROUP:
            payload["sequential_image_generation"] = "auto"
            payload["sequential_image_generation_options"] = {
                "max_images": request.max_images,
            }
        elif request.mode == AdImageMode.MULTI_FUSION:
            payload["sequential_image_generation"] = "disabled"

        return payload

    async def generate(self, request: AdImageRequest) -> AdImageResponse:
        images = await self._seedream.resolve_image_refs(request.images)
        payload = self.build_payload(request, images=images)
        logger.info(
            "ad image generate | mode=%s images=%d web_search=%s",
            request.mode.value,
            len(request.images),
            request.web_search,
        )
        raw = await self._seedream.generate(payload)
        return self._to_response(request.mode, raw)

    async def generate_stream(
        self, request: AdImageRequest
    ) -> AsyncIterator[dict[str, Any]]:
        images = await self._seedream.resolve_image_refs(request.images)
        payload = self.build_payload(request, images=images)
        logger.info("ad image stream | mode=%s", request.mode.value)
        async for event in self._seedream.generate_stream(payload):
            yield event

    @staticmethod
    def _to_response(mode: AdImageMode, raw: dict[str, Any]) -> AdImageResponse:
        items: list[AdImageItem] = []
        for row in raw.get("data") or []:
            if not isinstance(row, dict):
                continue
            items.append(
                AdImageItem(
                    url=str(row.get("url") or ""),
                    b64_json=str(row.get("b64_json") or ""),
                    revised_prompt=str(row.get("revised_prompt") or ""),
                )
            )
        return AdImageResponse(
            mode=mode,
            created=raw.get("created"),
            images=items,
            usage=raw.get("usage") if isinstance(raw.get("usage"), dict) else None,
        )
