import logging

from fastapi import FastAPI
from requests import Request
from starlette.middleware.base import RequestResponseEndpoint

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.middleware("http")
async def logging_middleware(request: Request, call_next: RequestResponseEndpoint):
    response = await call_next(request)
    logger.debug(f"{request.method} {request.url.path} {response.status_code}")
    return response


@app.post("/posts")
async def create_post():
    return {"message": "post created"}


@app.get("/posts")
async def get_post_list():
    return {"message": "post list"}


@app.post("/friends")
async def add_friend():
    return {"message": "friend added"}


@app.put("/like")
async def like_post():
    return {"message": "post liked"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=9999, reload=True)
