from typing import Any

from fastapi import FastAPI, Body, Depends
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from consistent_hash.consistent_hash import ConsistentHash, CacheServer, CacheIsFullException, Key, Value

app = FastAPI()


async def get_cache_server(request: Request, key: str = Body()) -> CacheServer:
    cache_servers = request.state.consistent_hash.get_node_by_key(key)
    return cache_servers


async def get_consistent_hash(request: Request) -> ConsistentHash:
    return request.state.consistent_hash


@app.on_event("startup")
async def startup():
    app.state.consistent_hash = ConsistentHash([CacheServer()])


@app.post("/read", status_code=status.HTTP_200_OK)
async def read(response: Response, key: str = Body(), cache_server: CacheServer = Depends(get_cache_server),
               consistent_hash: ConsistentHash = Depends(get_consistent_hash)):
    response.headers["X-CacheServer-Index"] = str(cache_server.id)
    response.headers["X-CacheServer-Count"] = str(consistent_hash.number_of_nodes)
    return cache_server.get(Key(key))


@app.post("/write", status_code=status.HTTP_201_CREATED)
async def write(response: Response, key: str = Body(), value: str = Body(),
                cache_server: CacheServer = Depends(get_cache_server),
                consistent_hash: ConsistentHash = Depends(get_consistent_hash)):
    try:
        cache_server.set(Key(key), Value(value))
    except CacheIsFullException:
        new_cache_server = CacheServer()
        consistent_hash.add_node(new_cache_server)
        new_cache_server.set(Key(key), Value(value))

    response.headers["X-CacheServer-Index"] = str(cache_server.id)
    response.headers["X-CacheServer-Count"] = str(consistent_hash.number_of_nodes)
