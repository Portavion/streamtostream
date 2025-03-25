from fastapi import APIRouter, Depends
from .handlers import convert_track_id
from models import StreamingPlatform
from ..utils import validate_platform_id
from urllib.parse import quote

router = APIRouter()


@router.get("/convert/track/{id}", tags=["metadata"])
async def convert_track(
    id: str, platform: StreamingPlatform = Depends(validate_platform_id)
):
    streaming_links = await convert_track_id(quote(id), platform)
    return {"links": streaming_links}
