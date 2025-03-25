from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .convert_track import router as track_router
from .convert_album import router as album_router

app = FastAPI()

origins = ["http://localhost", "http://localhost:5173", "https://streamto.stream"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(track_router.router, prefix="/api/v1")
app.include_router(album_router.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Hello World"}
