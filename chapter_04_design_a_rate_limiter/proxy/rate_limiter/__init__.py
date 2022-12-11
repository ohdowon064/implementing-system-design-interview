from typing import NewType, NamedTuple

from proxy.rate_limiter.token_bucket import TokenBucket


class RequestType(NamedTuple):
    path: str
    method: str


endpoint_rate_limiter: dict[RequestType, TokenBucket] = {}
