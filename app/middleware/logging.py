import logging
import time
from fastapi import Request

logger = logging.getLogger("arrenda.access")
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)


async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000

    logger.info(
        "%s %s %d %.1fms | ip=%s",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
        request.client.host if request.client else "-",
    )
    return response
