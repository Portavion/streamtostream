from .models import Album, StreamingPlatform
from .services.tidal import (
    get_isrc_tidal,
    get_tidal_track_link,
    get_tidal_album_link,
    get_album_info_tidal,
)
from .services.spotify import (
    get_isrc_spotify,
    get_spotify_track_link_by_isrc,
    get_spotify_album_link,
    get_album_info_spotify,
)


async def convert_track_id(id: str) -> list[str]:
    """Convert a track id to a list of links for other various streaming platforms (supports: Spotify and Tidal)"""
    return await get_track_streaming_links(id)


async def convert_album_id(id: str) -> list[str]:
    """Convert an album id to a list of links for other various streaming platforms (supports: Spotify and Tidal)"""
    return await get_album_streaming_links(id)


async def get_isrc_code(id: str) -> int:
    """Gets the ISRC code for the specified track id"""
    platform = StreamingPlatform.from_id(id)
    if platform == StreamingPlatform.TIDAL:
        return await get_isrc_tidal(id)
    elif platform == StreamingPlatform.SPOTIFY:
        return await get_isrc_spotify(id)

    raise ValueError(f"Unexpected platform: {platform}")


async def get_track_streaming_links(id: str) -> list[str]:
    """Gets the song streaming links for other platforms (supports Spotify and Tidal)"""
    platform = StreamingPlatform.from_id(id)
    isrc_code = await get_isrc_code(id)

    if platform == StreamingPlatform.SPOTIFY:
        return [await get_tidal_track_link(isrc_code)]
    elif platform == StreamingPlatform.TIDAL:
        return [await get_spotify_track_link_by_isrc(isrc_code)]

    raise ValueError(f"Unexpected platform: {platform}")


async def get_album_streaming_links(id: str) -> list[str]:
    """Gets the album streaming links for other platforms (supports Spotify and Tidal)"""
    platform = StreamingPlatform.from_id(id)
    album_info = await get_album_info(id)

    if platform == StreamingPlatform.SPOTIFY:
        return [await get_tidal_album_link(album_info)]
    elif platform == StreamingPlatform.TIDAL:
        return [await get_spotify_album_link(album_info)]

    raise ValueError(f"Unexpected platform: {platform}")


async def get_album_info(id: str) -> Album:
    """Gets the album information from an album id"""
    platform = StreamingPlatform.from_id(id)
    if platform == StreamingPlatform.TIDAL:
        return await get_album_info_tidal(id)
    elif platform == StreamingPlatform.SPOTIFY:
        return await get_album_info_spotify(id)

    raise ValueError(f"Unexpected platform: {platform}")
