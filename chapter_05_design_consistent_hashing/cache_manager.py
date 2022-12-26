import requests
from pydantic import BaseModel


class RequestResult(BaseModel):
    cache_server_index: int
    cache_server_count: int
    cache_server_indexes: str
    ring_distribution: str


class ReadResult(RequestResult):
    value: str | None


class CacheManager:
    def __init__(self):
        self._SERVER_ADDR = "http://localhost:9999"

    def read(self, key: str) -> ReadResult:
        res = requests.get(f"{self._SERVER_ADDR}/{key}", timeout=3)
        result = ReadResult(
            cache_server_index=res.headers["X-CacheServer-Index"],
            cache_server_count=res.headers["X-CacheServer-Count"],
            cache_server_indexes=res.headers["X-CacheServer-Indexes"],
            ring_distribution=res.headers["X-Ring-Distribution"],
        )
        if res.status_code == 200:
            result.value = res.json()["value"]
            return result
        return result

    def set(self, key: str, value: str) -> RequestResult:
        res = requests.post(
            f"{self._SERVER_ADDR}/{key}", json={"value": value}, timeout=3
        )
        return RequestResult(
            cache_server_index=res.headers["X-CacheServer-Index"],
            cache_server_count=res.headers["X-CacheServer-Count"],
            cache_server_indexes=res.headers["X-CacheServer-Indexes"],
            ring_distribution=res.headers["X-Ring-Distribution"],
        )


cache = CacheManager()
