import json
from collections.abc import AsyncIterator

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app.api.deps import get_ad_image_service
from app.prompts.ad_image import AD_IMAGE_OPENAPI_EXAMPLES
from app.schemas.ad_image import AdImageRequest, AdImageResponse
from app.services.ad_image import AdImageService

router = APIRouter(prefix="/ad", tags=["广告图片"])

_AD_IMAGE_BODY = Body(openapi_examples=AD_IMAGE_OPENAPI_EXAMPLES)


@router.post("/image", response_model=AdImageResponse)
async def generate_image(
    body: AdImageRequest = _AD_IMAGE_BODY,
    service: AdImageService = Depends(get_ad_image_service),
) -> AdImageResponse:
    """Seedream 5.0 lite 广告图片生成（非流式）。Swagger 请求体右上角可切换示例。"""
    try:
        return await service.generate(body)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/image/stream")
async def generate_image_stream(
    body: AdImageRequest = _AD_IMAGE_BODY,
    service: AdImageService = Depends(get_ad_image_service),
) -> StreamingResponse:
    """Seedream 5.0 lite 流式输出（SSE）。请求体示例与非流式接口相同。"""

    async def event_stream() -> AsyncIterator[str]:
        try:
            async for chunk in service.generate_stream(body):
                yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"
        except ValueError as exc:
            yield f"data: {json.dumps({'error': str(exc)}, ensure_ascii=False)}\n\n"
        except Exception as exc:
            yield f"data: {json.dumps({'error': str(exc)}, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
