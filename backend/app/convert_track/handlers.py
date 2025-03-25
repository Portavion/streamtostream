from ..models import StreamingPlatform
from .services.tidal import (
    get_isrc_tidal,
    get_tidal_track_link,
)
from .services.spotify import (
    get_isrc_spotify,
    get_spotify_track_link_by_isrc,
)


async def convert_track_id(id: str, platform: StreamingPlatform) -> list[str]:
    """Convert a track id to a list of links for other various streaming platforms (supports: Spotify and Tidal)"""
    isrc_code = await get_isrc_code(id, platform)

    if platform == StreamingPlatform.SPOTIFY:
        return [await get_tidal_track_link(isrc_code)]
    elif platform == StreamingPlatform.TIDAL:
        return [await get_spotify_track_link_by_isrc(isrc_code)]


async def get_isrc_code(id: str, platform: StreamingPlatform) -> int:
    """Gets the ISRC code for the specified track id"""
    if platform == StreamingPlatform.TIDAL:
        return await get_isrc_tidal(id)
    elif platform == StreamingPlatform.SPOTIFY:
        return await get_isrc_spotify(id)
