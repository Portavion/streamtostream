from fastapi import APIRouter, Depends
from .handlers import convert_album_id
from ..models import StreamingPlatform
from ..utils import validate_platform_id
from urllib.parse import quote

router = APIRouter()


@router.get("/convert/album/{id}", tags=["metadata"])
async def convert_album(
    id: str, platform: StreamingPlatform = Depends(validate_platform_id)
):
    streaming_links = await convert_album_id(quote(id), platform)
    return {"links": streaming_links}
