from fastapi import APIRouter
from .service import convert_track_link

router = APIRouter()


@router.get("/convert-link/{link:path}", tags=["metadata"])
async def convert_link(link: str):
    streaming_links = await convert_track_link(link)
    return {"links": streaming_links}
