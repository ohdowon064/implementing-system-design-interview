from typing import NamedTuple

from chapter_04_design_a_rate_limiter.proxy.rate_limiter.token_bucket import TokenBucket


class RequestType(NamedTuple):
    path: str
    method: str


endpoint_rate_limiter: dict[RequestType, TokenBucket] = {}
