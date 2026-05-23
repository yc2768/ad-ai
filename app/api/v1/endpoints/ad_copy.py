from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_ad_copy_service
from app.schemas.ad_copy import AdCopyItem, AdCopyRequest
from app.services.ad_copy import AdCopyService

router = APIRouter(prefix="/ad", tags=["广告文案"])


@router.post("/copy", response_model=list[AdCopyItem])
async def generate_copy(
    body: AdCopyRequest,
    service: AdCopyService = Depends(get_ad_copy_service),
) -> list[AdCopyItem]:
    try:
        return await service.generate(body)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
