# pylint: disable=unused-argument, import-error
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from cache_manager import cache

app = FastAPI()


@app.exception_handler(KeyError)
async def key_error_handler(request: Request, exc: KeyError):
    return JSONResponse(
        status_code=404,
        content={"message": "Key does not exist."},
    )


@app.get("/{key}", status_code=200)
async def read(response: Response, key: str):
    result = cache.read(key)
    response.headers["X-CacheServer-Index"] = str(result.cache_server_index)
    response.headers["X-CacheServer-Count"] = str(result.cache_server_count)
    response.headers["X-CacheServer-Indexes"] = result.cache_server_indexes
    response.headers["X-Ring-Distribution"] = result.ring_distribution
    if result.value is None:
        response.status_code = 404
    else:
        return result.dict(include={"value"})


class WriteRequest(BaseModel):
    value: str


@app.post("/{key}", status_code=201)
async def write(response: Response, key: str, request_body: WriteRequest):
    result = cache.set(key, request_body.value)
    response.headers["X-CacheServer-Index"] = str(result.cache_server_index)
    response.headers["X-CacheServer-Count"] = str(result.cache_server_count)
    response.headers["X-CacheServer-Indexes"] = result.cache_server_indexes
    response.headers["X-Ring-Distribution"] = result.ring_distribution
    return {"message": "Value set."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=True)
