import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.deps import get_doubao_service, get_seedance_service, get_seedream_service
from app.api.v1 import api_router
from app.core.config import settings
from app.core.docs import register_doc_routes
from app.core.exceptions import (
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from app.core.logging import setup_logging
from app.middleware import RequestLogMiddleware

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("application starting | %s v%s", settings.app_name, settings.app_version)
    logger.info("API docs  | %s/api/docs", settings.base_url)
    logger.info("Health    | %s/api/v1/health", settings.base_url)
    logger.info("Ad copy   | POST %s/api/v1/ad/copy", settings.base_url)
    logger.info("Ad image  | POST %s/api/v1/ad/image", settings.base_url)
    logger.info("Ad video  | POST %s/api/v1/ad/video", settings.base_url)
    yield
    await get_doubao_service().aclose()
    await get_seedream_service().aclose()
    await get_seedance_service().aclose()
    logger.info("application shutdown")


def create_app() -> FastAPI:
    openapi_url = "/api/openapi.json"
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
        docs_url=None,
        redoc_url=None,
        openapi_url=openapi_url,
    )

    register_doc_routes(app, title=settings.app_name, openapi_url=openapi_url)

    app.add_middleware(RequestLogMiddleware)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()
