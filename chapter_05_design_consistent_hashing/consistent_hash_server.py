# pylint: disable=import-error
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from consistent_hash import (CacheIsFullException, CacheServer, ConsistentHash,
                             Key, KeyDoesNotExistException, Value)

app = FastAPI()


async def get_consistent_hash(request: Request) -> ConsistentHash:
    return request.app.state.consistent_hash


async def get_cache_server(
    key: str, consistent_hash: ConsistentHash = Depends(get_consistent_hash)
) -> CacheServer:
    return consistent_hash.get_node_by_key(Key(key))


class WriteRequest(BaseModel):
    value: str


@app.on_event("startup")
async def startup():
    app.state.consistent_hash = ConsistentHash([CacheServer()])


@app.get("/{key}", status_code=status.HTTP_200_OK)
async def read(
    response: Response,
    key: str,
    consistent_hash: ConsistentHash = Depends(get_consistent_hash),
    cache_server: CacheServer = Depends(get_cache_server),
):
    response.headers["X-CacheServer-Index"] = str(cache_server.id)
    response.headers["X-CacheServer-Count"] = str(consistent_hash.number_of_nodes)

    try:
        value = cache_server.get(Key(key))
    except KeyDoesNotExistException:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Key does not exist."}
    else:
        return {"value": value}


@app.post("/{key}", status_code=status.HTTP_201_CREATED)
async def write(
    response: Response,
    key: str,
    request_body: WriteRequest,
    cache_server: CacheServer = Depends(get_cache_server),
    consistent_hash: ConsistentHash = Depends(get_consistent_hash),
):
    try:
        cache_server.set(Key(key), Value(request_body.value))
    except CacheIsFullException:
        new_cache_server = CacheServer()
        consistent_hash.add_node(new_cache_server)
        new_cache_server.set(Key(key), request_body.value)

    response.headers["X-CacheServer-Index"] = str(cache_server.id)
    response.headers["X-CacheServer-Count"] = str(consistent_hash.number_of_nodes)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("consistent_hash_server:app", host="0.0.0.0", port=8000, reload=True)
