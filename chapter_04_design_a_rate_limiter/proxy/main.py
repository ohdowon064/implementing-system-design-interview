import httpx
from httpx import AsyncClient
from fastapi import Request, FastAPI
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTask
from starlette.middleware import Middleware

from chapter_04_design_a_rate_limiter.proxy.config import settings
from chapter_04_design_a_rate_limiter.proxy.middleware.rate_limiter import RateLimitMiddleware

app = FastAPI(middleware=[Middleware(RateLimitMiddleware)])
http_client = AsyncClient(base_url=f"http://{settings.api_server_host}:{settings.api_server_port}/")


async def _reverse_proxy(request: Request):
    url = httpx.URL(path=request.url.path, query=request.url.query.encode("utf-8"))
    api_request = http_client.build_request(
        request.method, url, headers=request.headers.raw, content=await request.body()
    )
    api_response = await http_client.send(api_request, stream=True)
    return StreamingResponse(
        api_response.aiter_raw(),
        status_code=api_response.status_code,
        headers=api_response.headers,
        background=BackgroundTask(api_response.aclose),
    )


app.add_route("/{path:path}", _reverse_proxy, ["GET", "POST"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
