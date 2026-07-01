import time
import uuid
from collections import defaultdict

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.logging import get_logger

logger = get_logger(__name__)

_rate_buckets: dict[str, list[float]] = defaultdict(list)
RATE_LIMIT = 120
RATE_WINDOW_SEC = 60


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        start = time.perf_counter()

        client_key = request.client.host if request.client else "unknown"
        if request.url.path.startswith("/v1/auth") or "/reflection/message" in request.url.path:
            now = time.time()
            bucket = _rate_buckets[client_key]
            bucket[:] = [t for t in bucket if now - t < RATE_WINDOW_SEC]
            if len(bucket) >= RATE_LIMIT:
                return Response("Too many requests", status_code=429, headers={"Retry-After": "60"})
            bucket.append(now)

        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000
        response.headers["X-Request-ID"] = request_id
        logger.info(
            "request",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration_ms=round(elapsed_ms, 2),
        )
        return response