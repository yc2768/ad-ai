from fastapi import APIRouter, Body, Depends, HTTPException

from app.api.deps import get_ad_video_service
from app.prompts.ad_video import AD_VIDEO_OPENAPI_EXAMPLES
from app.schemas.ad_video import AdVideoRequest, AdVideoResponse
from app.services.ad_video import AdVideoService

router = APIRouter(prefix="/ad", tags=["广告视频"])

_AD_VIDEO_BODY = Body(openapi_examples=AD_VIDEO_OPENAPI_EXAMPLES)


@router.post("/video", response_model=AdVideoResponse)
async def generate_video(
    body: AdVideoRequest = _AD_VIDEO_BODY,
    service: AdVideoService = Depends(get_ad_video_service),
) -> AdVideoResponse:
    """Seedance 2.0 异步提交视频任务，立即返回 task_id；参考 [创建视频任务 API](https://www.volcengine.com/docs/82379/1520757?lang=zh)。"""
    try:
        return await service.generate(body)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/video/{task_id}", response_model=AdVideoResponse)
async def get_video_task(
    task_id: str,
    service: AdVideoService = Depends(get_ad_video_service),
) -> AdVideoResponse:
    """查询视频生成任务状态（POST 提交后轮询此接口）。"""
    try:
        return await service.get_task(task_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
