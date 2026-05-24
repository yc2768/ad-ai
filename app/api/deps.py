from functools import lru_cache

from app.core.config import settings
from app.services.ad_copy import AdCopyService
from app.services.ad_image import AdImageService
from app.services.ad_video import AdVideoService
from app.services.doubao import DoubaoService
from app.services.health_service import HealthService
from app.services.seedance import SeedanceService
from app.services.seedream import SeedreamService


@lru_cache
def get_health_service() -> HealthService:
    return HealthService()


@lru_cache
def get_doubao_service() -> DoubaoService:
    return DoubaoService(cfg=settings)


@lru_cache
def get_ad_copy_service() -> AdCopyService:
    return AdCopyService(doubao=get_doubao_service())


@lru_cache
def get_seedream_service() -> SeedreamService:
    return SeedreamService(cfg=settings)


@lru_cache
def get_ad_image_service() -> AdImageService:
    return AdImageService(seedream=get_seedream_service())


@lru_cache
def get_seedance_service() -> SeedanceService:
    return SeedanceService(cfg=settings)


@lru_cache
def get_ad_video_service() -> AdVideoService:
    return AdVideoService(
        seedance=get_seedance_service(),
        seedream=get_seedream_service(),
    )
