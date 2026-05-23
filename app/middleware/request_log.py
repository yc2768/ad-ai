import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("app.request")


class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id

        start = time.perf_counter()
        logger.info(
            "request started | %s %s",
            request.method,
            request.url.path,
            extra={"request_id": request_id},
        )

        try:
            response = await call_next(request)
        except Exception:
            duration_ms = (time.perf_counter() - start) * 1000
            logger.exception(
                "request failed | %s %s | %.2fms",
                request.method,
                request.url.path,
                duration_ms,
                extra={"request_id": request_id},
            )
            raise

        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "request finished | %s %s | status=%s | %.2fms",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
            extra={"request_id": request_id},
        )

        response.headers["X-Request-ID"] = request_id
        return response
