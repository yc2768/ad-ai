from fastapi import APIRouter, Depends

from app.api.deps import get_health_service
from app.schemas.common import ApiResponse, HealthData
from app.services.health_service import HealthService

router = APIRouter(tags=["health"])


@router.get("/health", response_model=ApiResponse[HealthData])
def health_check(
    service: HealthService = Depends(get_health_service),
) -> ApiResponse[HealthData]:
    return ApiResponse(data=service.check())
