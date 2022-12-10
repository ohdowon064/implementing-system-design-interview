import logging

from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from proxy.rate_limiter import endpoint_rate_limiter, TokenBucket, RequestType

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.DEBUG)
logging.getLogger("httpx").setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_type = RequestType(path=request.url.path, method=request.method)

        if request_type in endpoint_rate_limiter:
            rate_limiter = endpoint_rate_limiter[request_type]
        else:
            rate_limiter = TokenBucket()
            endpoint_rate_limiter[request_type] = rate_limiter

        if rate_limiter.consume():
            response = await call_next(request)
        else:
            response = Response(status_code=status.HTTP_429_TOO_MANY_REQUESTS)

        logger.debug(endpoint_rate_limiter)
        response.headers["X-Ratelimit-Remaining"] = str(rate_limiter.get_remaining_tokens())
        response.headers["X-Ratelimit-Limit"] = str(rate_limiter.get_capacity())
        response.headers["X-Ratelimit-Retry-After"] = str(rate_limiter.get_refill_period())
        return response
