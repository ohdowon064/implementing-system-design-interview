from fastapi import FastAPI

app = FastAPI()


@app.get("/resource")
async def get_resource():
    return {"message": "OK"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=9999, reload=True)
