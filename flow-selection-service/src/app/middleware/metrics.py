import logging
import time
import uuid

from fastapi import Request

from app.config.metrics import http_request_duration_seconds, http_requests_total

logger = logging.getLogger(__name__)

def generate_request_id() -> str:
    """Генерирует короткий request_id (16 символов)."""
    return uuid.uuid4().hex[:16]

async def metrics_middleware(request: Request, call_next, service_name: str):  # type: ignore[no-untyped-def]

    start_time = time.time()
    try:
        response = await call_next(request)
        status = response.status_code
    except Exception:
        status = 500
        raise
    finally:
        duration = time.time() - start_time
        http_requests_total.labels(
            method=request.method,
            endpoint=request.url.path,
            status=status,
            service_name=service_name
        ).inc()
        http_request_duration_seconds.labels(
            method=request.method,
            endpoint=request.url.path,
            service_name=service_name
        ).observe(duration)

    return response
