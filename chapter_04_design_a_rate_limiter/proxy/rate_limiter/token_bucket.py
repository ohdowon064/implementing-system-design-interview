import time

from chapter_04_design_a_rate_limiter.proxy.config import settings


class TokenBucket:
    def __init__(self):
        self._capacity: int = settings.capacity
        self._refill_period: int = settings.refill_period
        self._number_of_refilled_tokens_per_period: int = settings.number_of_refilled_tokens_per_period
        self._tokens: int = self._capacity
        self._last_refill_time = int(time.time())

    def _is_empty(self) -> bool:
        return self._tokens < 1

    def consume(self, tokens: int = 1) -> bool:
        self._refill()
        if not self._is_empty():
            self._tokens -= tokens
            return True
        return False

    def get_remaining_tokens(self) -> float:
        return self._tokens

    def get_capacity(self) -> int:
        return self._capacity

    def get_refill_period(self) -> int:
        return self._refill_period

    def _get_refilled_tokens(self, elapsed: int) -> int:
        refill_count = elapsed // self._refill_period
        return refill_count * self._number_of_refilled_tokens_per_period

    def _refill(self) -> None:
        now = int(time.time())
        elapsed = now - self._last_refill_time
        if elapsed >= self._refill_period:
            self._last_refill_time = now
            self._tokens = min(self._capacity, self._tokens + self._get_refilled_tokens(elapsed))

    def __repr__(self):
        return self.__dict__.__repr__()
