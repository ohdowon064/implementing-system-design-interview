from fastapi import FastAPI

from consistent_hash.dto import ReadRequest, WriteRequest

app = FastAPI()


@app.post("/read")
async def read(request_data: ReadRequest):
    ...


@app.post("/write")
async def write(request_data: WriteRequest):
    ...
