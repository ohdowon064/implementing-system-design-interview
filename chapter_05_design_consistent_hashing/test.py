import requests


def test_x_cache_server_index():
    res = requests.post(
        "http://localhost:8000/key1", json={"value": "value1"}, timeout=1
    )
    index, indexes = (
        res.headers["X-CacheServer-Index"],
        res.headers["X-CacheServer-Indexes"],
    )
    assert res.status_code == 201
    assert index in indexes


def test_ring_distribution():
    success_keys = []
    for i in range(100):
        res = requests.post(
            f"http://localhost:8000/key{i}", json={"value": "value"}, timeout=1
        )
        if res.status_code == 201:
            success_keys.append(f"key{i}")

    indexes = {index: 0 for index in res.headers["X-CacheServer-Indexes"].split(",")}

    error_count = 0
    for i in range(100):
        res = requests.get(f"http://localhost:8000/key{i}", timeout=1)
        if res.status_code == 200:
            index = res.headers["X-CacheServer-Index"]
            indexes[index] += 1
        else:
            error_count += 1

    print(indexes.values())
    print(error_count)


if __name__ == "__main__":
    test_x_cache_server_index()
    test_ring_distribution()
