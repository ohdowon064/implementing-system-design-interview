from fastapi import FastAPI

app = FastAPI()


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
