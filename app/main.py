import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.deps import get_doubao_service
from app.api.v1 import api_router
from app.core.config import settings
from app.core.exceptions import unhandled_exception_handler
from app.core.logging import setup_logging
from app.middleware import RequestLogMiddleware

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("application starting | %s v%s", settings.app_name, settings.app_version)
    yield
    await get_doubao_service().aclose()
    logger.info("application shutdown")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    app.add_middleware(RequestLogMiddleware)
    app.add_exception_handler(Exception, unhandled_exception_handler)
    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()
