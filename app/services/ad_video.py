import logging
from typing import Any

from app.schemas.ad_video import AdVideoMode, AdVideoRequest, AdVideoResponse
from app.services.seedance import SeedanceService
from app.services.seedream import SeedreamService

logger = logging.getLogger(__name__)


class AdVideoService:
    """广告视频提效：Seedance 2.0 多模态参考（文本 + 视频 + 图片）。"""

    def __init__(
        self,
        seedance: SeedanceService,
        seedream: SeedreamService,
    ) -> None:
        self._seedance = seedance
        self._seedream = seedream

    def build_payload(
        self,
        request: AdVideoRequest,
        *,
        image_url: str,
    ) -> dict[str, Any]:
        content: list[dict[str, Any]] = [
            {"type": "text", "text": request.prompt},
            {
                "type": "video_url",
                "video_url": {"url": request.video_url.strip()},
                "role": "reference_video",
            },
            {
                "type": "image_url",
                "image_url": {"url": image_url},
                "role": "reference_image",
            },
        ]

        return {
            "model": self._seedance.resolve_model(request.model),
            "content": content,
            "ratio": request.ratio,
            "duration": request.duration,
            "resolution": request.resolution,
            "watermark": request.watermark,
            "generate_audio": request.generate_audio,
        }

    async def generate(self, request: AdVideoRequest) -> AdVideoResponse:
        resolved_images = await self._seedream.resolve_image_refs([request.image_url])
        image_ref = resolved_images[0]
        payload = self.build_payload(request, image_url=image_ref)

        logger.info(
            "ad video create | mode=%s model=%s",
            request.mode.value,
            payload["model"],
        )
        created = await self._seedance.create_task(payload)
        task_id = str(created.get("id", ""))
        if not task_id:
            raise ValueError("方舟未返回任务 ID")

        return AdVideoResponse(
            mode=request.mode,
            task_id=task_id,
            status=str(created.get("status", "queued")),
            message="任务已提交，请 GET /api/v1/ad/video/{task_id} 查询结果",
        )

    async def get_task(self, task_id: str, *, mode: AdVideoMode = AdVideoMode.PRODUCT_REPLACE) -> AdVideoResponse:
        result = await self._seedance.get_task(task_id)
        status = str(result.get("status", ""))
        video_url = ""
        message = ""
        if status == "succeeded":
            video_url = self._seedance.extract_video_url(result)
            message = "生成成功，视频 URL 约 24 小时内有效，请及时下载"
        elif status in ("failed", "expired", "cancelled"):
            err = result.get("error")
            message = str(err) if err else status

        usage = result.get("usage") if isinstance(result.get("usage"), dict) else None
        return AdVideoResponse(
            mode=mode,
            task_id=task_id,
            status=status,
            video_url=video_url,
            usage=usage,
            message=message,
        )
