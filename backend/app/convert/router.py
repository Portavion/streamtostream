from fastapi import APIRouter
from .handlers import convert_track_id
from .handlers import convert_album_id

router = APIRouter()


@router.get("/convert/track/{id}", tags=["metadata"])
async def convert_track(id: str):
    streaming_links = await convert_track_id(id)
    return {"links": streaming_links}


@router.get("/convert/album/{id}", tags=["metadata"])
async def convert_album(id: str):
    streaming_links = await convert_album_id(id)
    return {"links": streaming_links}
