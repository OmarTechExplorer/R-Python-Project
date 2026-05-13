import time
import logging
from fastapi import Request
from starlette.responses import Response

from app.monitoring.metrics import record_request


logger = logging.getLogger("library.middleware")


async def log_requests(request: Request, call_next) -> Response:
    start_time = time.time()

    try:
        response = await call_next(request)
    except Exception as e:
        duration = round(time.time() - start_time, 3)
        logger.error(
            f"{request.method} {request.url.path} | "
            f"status: 500 | duration: {duration}s | error: {e}"
        )
        record_request(500)
        raise

    duration = round(time.time() - start_time, 3)

    record_request(response.status_code)

    logger.info(
        f"{request.method} {request.url.path} | "
        f"status: {response.status_code} | "
        f"duration: {duration}s"
    )

    return response