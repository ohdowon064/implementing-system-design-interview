from fastapi import FastAPI

app = FastAPI()


@app.post("/resource")
async def create_resource():
    return {"message": "Created"}


@app.get("/resource")
async def get_resource():
    return {"message": "OK"}


@app.put("/resource")
async def update_resource():
    return {"message": "Updated"}
