import logging

from app.core.config import settings
from app.schemas.common import HealthData

logger = logging.getLogger(__name__)


class HealthService:
    def check(self) -> HealthData:
        logger.debug("health check")
        return HealthData(
            status="ok",
            app_name=settings.app_name,
            version=settings.app_version,
        )
