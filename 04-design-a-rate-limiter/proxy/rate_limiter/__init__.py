from typing import NewType

from proxy.rate_limiter.token_bucket import TokenBucket

RequestPath = NewType("RequestPath", str)
endpoint_rate_limiter: dict[RequestPath, TokenBucket] = {}
