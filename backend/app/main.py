from fastapi import FastAPI

from .convert_link import router

app = FastAPI()

app.include_router(router.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Hello World"}
