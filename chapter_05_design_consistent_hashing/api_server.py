# pylint: disable=unused-argument, import-error
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse

from cache_manager import cache

app = FastAPI()


@app.exception_handler(KeyError)
async def key_error_handler(request: Request, exc: KeyError):
    return JSONResponse(
        status_code=404,
        content={"message": "Key does not exist."},
    )


@app.get("/{key}")
async def read(key: str):
    return cache.read(key)


class WriteRequest(BaseModel):
    value: str


@app.post("/{key}")
async def write(key: str, request_body: WriteRequest):
    cache.set(key, request_body.value)
    return {"message": "Value set."}
