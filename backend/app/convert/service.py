import requests
from .auth_spotify import get_spotify_access_token
from .auth_tidal import get_tidal_access_token
from typing import Optional
from .models import Album, StreamingPlatform


class APIError(Exception):
    """Custom exception for API-related errors."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


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


async def get_isrc_tidal(tidal_id: str) -> int:
    """Gets the song ISRC code from a tidal track id"""
    access_token = get_tidal_access_token()
    if not access_token:
        raise APIError("Failed to retrieve Tidal access token.")

    headers = {"Authorization": f"Bearer {access_token}"}
    request_url = f"https://openapi.tidal.com/v2/tracks/{tidal_id}?countryCode=GB"

    response = requests.get(request_url, headers=headers).json()
    try:
        return response["data"]["attributes"]["isrc"]
    except (KeyError, TypeError):
        raise APIError(f"ISRC not found in Tidal response for track ID {tidal_id}")


async def get_isrc_spotify(spotify_id: str) -> int:
    """Gets the song ISRC code from a Spotify track id"""
    access_token = get_spotify_access_token()
    if not access_token:
        raise APIError("Failed to retrieve Spotify access token.")

    headers = {"Authorization": f"Bearer {access_token}"}
    request_url = f"https://api.spotify.com/v1/tracks/{spotify_id}"

    response = requests.get(request_url, headers=headers).json()

    try:
        return response["external_ids"]["isrc"]
    except (KeyError, TypeError):
        raise APIError(f"ISRC not found in Tidal response for track ID {spotify_id}")


async def get_spotify_track_link_by_isrc(isrc: int) -> str:
    """Gets a Spotify song link from song ISRC code"""
    access_token = get_spotify_access_token()
    if not access_token:
        raise APIError("Failed to retrieve Spotify access token.")

    headers = {"Authorization": f"Bearer {access_token}"}
    request_url = f"https://api.spotify.com/v1/search?q=isrc:{isrc}&type=track"
    response = requests.get(request_url, headers=headers).json()

    try:
        return response["tracks"]["items"][0]["external_urls"]["spotify"]
    except (KeyError, TypeError):
        raise APIError(f"Spotify link not found for ISRC: {isrc}")


async def get_tidal_track_link(isrc: int) -> str:
    """Gets a Tidal song link from song ISRC code"""
    access_token = get_tidal_access_token()
    if not access_token:
        raise APIError("Failed to retrieve Tidal access token.")

    headers = {"Authorization": f"Bearer {access_token}"}
    request_url = f"https://openapi.tidal.com/v2/tracks?countryCode=GB&include=albums&filter%5Bisrc%5D={isrc}&filter%5Bid%5D=251380837"
    response = requests.get(request_url, headers=headers).json()

    try:
        return response["data"][0]["attributes"]["externalLinks"][0]["href"]
    except (KeyError, TypeError):
        raise APIError(f"Tidal link not found for ISRC: {isrc}")


async def get_album_info_tidal(tidal_id: str) -> Album:
    """Get album informations from Tidal"""
    access_token = get_tidal_access_token()
    if not access_token:
        raise APIError("Failed to retrieve Tidal access token.")

    headers = {"Authorization": f"Bearer {access_token}"}
    request_url = (
        f"https://openapi.tidal.com/v2/albums/{tidal_id}?countryCode=GB&include=artists"
    )

    response = requests.get(request_url, headers=headers).json()
    album_title = response["data"]["attributes"]["title"]
    album_release_date = response["data"]["attributes"]["releaseDate"]
    album_artist = response["included"][0]["attributes"]["name"]
    album_upc = response["data"]["attributes"]["barcodeId"]

    try:
        return Album(
            **{
                "artist": album_artist,
                "album_name": album_title,
                "release_date": album_release_date,
                "upc": album_upc,
            }
        )
    except (KeyError, TypeError, IndexError):
        raise APIError(f"Failed to parse Tidal album info for album ID {tidal_id}")


async def get_album_info_spotify(spotify_id: str) -> Album:
    """Get album informations from Spotify"""
    access_token = get_spotify_access_token()
    if not access_token:
        raise APIError("Failed to retrieve Spotify access token.")

    headers = {"Authorization": f"Bearer {access_token}"}
    request_url = f"https://api.spotify.com/v1/albums/{spotify_id}"

    response = requests.get(request_url, headers=headers).json()
    album_title = response["name"]
    album_release_date = response["release_date"]
    album_artist = response["artists"][0]["name"]
    album_upc = response["external_ids"]["upc"]

    try:
        return Album(
            **{
                "artist": album_artist,
                "album_name": album_title,
                "release_date": album_release_date,
                "upc": album_upc,
            }
        )
    except (KeyError, TypeError, IndexError):
        raise APIError(f"Failed to parse Spotify album info for album ID {spotify_id}")


async def get_tidal_album_link(album_info: Album) -> str:
    """Gets a Tidal album link from the album UPC code"""
    access_token = get_tidal_access_token()
    if not access_token:
        raise APIError("Failed to retrieve Tidal access token.")

    headers = {"Authorization": f"Bearer {access_token}"}
    request_url = f"https://openapi.tidal.com/v2/albums?countryCode=GM&include=artists&include=items&filter%5BbarcodeId%5D={album_info.upc}"
    response = requests.get(request_url, headers=headers).json()

    try:
        return response["data"][0]["attributes"]["externalLinks"][0]["href"]
    except (KeyError, IndexError, TypeError):
        raise APIError(f"Tidal album link not found for UPC {album_info.upc}")


async def get_spotify_album_link(album_info: Album) -> str:
    """Gets a Spotify album link from the album UPC code"""
    access_token = get_spotify_access_token()
    if not access_token:
        raise APIError("Failed to retrieve Spotify access token.")

    headers = {"Authorization": f"Bearer {access_token}"}
    request_url = (
        f"https://api.spotify.com/v1/search?q=upc%3A{album_info.upc}&type=album"
    )
    response = requests.get(request_url, headers=headers).json()

    try:
        return response["albums"]["items"][0]["external_urls"]["spotify"]
    except (KeyError, IndexError, TypeError):
        raise APIError(f"Tidal album link not found for UPC {album_info.upc}")
