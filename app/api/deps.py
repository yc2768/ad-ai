from functools import lru_cache

from app.core.config import settings
from app.services.ad_copy import AdCopyService
from app.services.doubao import DoubaoService
from app.services.health_service import HealthService


@lru_cache
def get_health_service() -> HealthService:
    return HealthService()


@lru_cache
def get_doubao_service() -> DoubaoService:
    return DoubaoService(cfg=settings)


@lru_cache
def get_ad_copy_service() -> AdCopyService:
    return AdCopyService(doubao=get_doubao_service())
