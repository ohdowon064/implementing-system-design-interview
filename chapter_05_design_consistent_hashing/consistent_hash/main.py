from fastapi import FastAPI
from starlette.requests import Request

from consistent_hash.consistent_hash import ConsistentHash, CacheServer
from consistent_hash.dto import ReadRequest, WriteRequest

app = FastAPI()


@app.on_event("startup")
async def startup(request: Request):
    request.state.consistent_hash = ConsistentHash([CacheServer()])

@app.post("/read")
async def read(request_data: ReadRequest):
    ...


@app.post("/write")
async def write(request_data: WriteRequest):
    ...
