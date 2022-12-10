import httpx
from httpx import AsyncClient
from fastapi import Request, FastAPI
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTask

app = FastAPI()
http_client = AsyncClient(base_url="http://0.0.0.0:9999/")


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
