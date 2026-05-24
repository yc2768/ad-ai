import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.schemas.common import ApiResponse

logger = logging.getLogger(__name__)


def _format_http_detail(detail: object) -> str:
    if isinstance(detail, str):
        return detail
    if isinstance(detail, list):
        parts: list[str] = []
        for item in detail:
            if isinstance(item, dict):
                loc = ".".join(str(x) for x in item.get("loc", ()))
                msg = item.get("msg", "")
                parts.append(f"{loc}: {msg}" if loc else str(msg))
            else:
                parts.append(str(item))
        return "; ".join(parts) if parts else str(detail)
    return str(detail)


async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    message = _format_http_detail(exc.detail)
    body = ApiResponse(code=exc.status_code, message=message, data=None)
    return JSONResponse(status_code=exc.status_code, content=body.model_dump())


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    message = _format_http_detail(exc.errors())
    body = ApiResponse(code=422, message=message, data=None)
    return JSONResponse(status_code=422, content=body.model_dump())


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "-")
    logger.exception("unhandled error | request_id=%s", request_id)
    body = ApiResponse(code=500, message="internal server error", data=None)
    return JSONResponse(status_code=500, content=body.model_dump())
