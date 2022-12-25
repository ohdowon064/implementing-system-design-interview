import requests


class CacheManager:
    def __init__(self):
        self._SERVER_ADDR = "http://localhost:9999"

    def read(self, key: str) -> str:
        res = requests.get(f"self._SERVER_ADDR/{key}")
        if res.status_code == 404:
            raise KeyError("Key does not exist")
        return res.json()["value"]

    def set(self, key: str, value: str) -> None:
        requests.post(f"self._SERVER_ADDR/{key}", json={"value": value})


cache = CacheManager()
