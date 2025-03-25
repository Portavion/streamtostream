from ..models import Album, StreamingPlatform
from .services.tidal import (
    get_tidal_album_link,
    get_album_info_tidal,
)
from .services.spotify import (
    get_spotify_album_link,
    get_album_info_spotify,
)


async def convert_album_id(id: str, platform: StreamingPlatform) -> list[str]:
    """Convert an album id to a list of links for other various streaming platforms (supports: Spotify and Tidal)"""
    album_info = await get_album_info(id, platform)

    if platform == StreamingPlatform.SPOTIFY:
        return [await get_tidal_album_link(album_info)]
    elif platform == StreamingPlatform.TIDAL:
        return [await get_spotify_album_link(album_info)]


async def get_album_info(id: str, platform: StreamingPlatform) -> Album:
    """Gets the album information from an album id"""
    if platform == StreamingPlatform.TIDAL:
        return await get_album_info_tidal(id)
    elif platform == StreamingPlatform.SPOTIFY:
        return await get_album_info_spotify(id)
