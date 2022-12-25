import requests
from pydantic import BaseModel


class RequestResult(BaseModel):
    cache_server_index: int
    cache_server_count: int


class ReadResult(RequestResult):
    value: str


class CacheManager:
    def __init__(self):
        self._SERVER_ADDR = "http://localhost:9999"

    def read(self, key: str) -> ReadResult:
        res = requests.get(f"{self._SERVER_ADDR}/{key}", timeout=3)
        if res.status_code == 404:
            raise KeyError("Key does not exist")
        return ReadResult(
            cache_server_index=res.headers["X-CacheServer-Index"],
            cache_server_count=res.headers["X-CacheServer-Count"],
            value=res.json()["value"],
        )

    def set(self, key: str, value: str) -> RequestResult:
        res = requests.post(
            f"{self._SERVER_ADDR}/{key}", json={"value": value}, timeout=3
        )
        return RequestResult(
            cache_server_index=res.headers["X-CacheServer-Index"],
            cache_server_count=res.headers["X-CacheServer-Count"],
        )


cache = CacheManager()
