import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from app.schemas.common import ApiResponse

logger = logging.getLogger(__name__)


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "-")
    logger.exception("unhandled error | request_id=%s", request_id)
    body = ApiResponse(code=500, message="internal server error", data=None)
    return JSONResponse(status_code=500, content=body.model_dump())
