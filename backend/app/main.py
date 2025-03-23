from fastapi import FastAPI

from .routers import convert_link

app = FastAPI()

app.include_router(convert_link.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Hello World"}
