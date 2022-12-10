import time

from proxy.config import settings


class TokenBucket:
    def __init__(self):
        self._capacity = settings.capacity
        self._number_of_refilled_tokens_per_second = settings.number_of_refilled_tokens_per_second
        self._tokens = self._capacity
        self._last_refill_time = int(time.time())

    def _is_empty(self):
        return self._tokens == 0

    def consume(self, tokens: int = 1) -> bool:
        self._refill()
        if not self._is_empty():
            self._tokens -= tokens
            return True
        return False

    def _refill(self):
        now = int(time.time())
        elapsed = now - self._last_refill_time
        self._last_refill_time = now
        self._tokens = min(self._capacity, self._tokens + elapsed * self._number_of_refilled_tokens_per_second)
