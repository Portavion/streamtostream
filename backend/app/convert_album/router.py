from fastapi import APIRouter
from .handlers import convert_album_id

router = APIRouter()


@router.get("/convert/album/{id}", tags=["metadata"])
async def convert_album(id: str):
    streaming_links = await convert_album_id(id)
    return {"links": streaming_links}
