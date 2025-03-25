import requests
from ..exceptions import APIError
from ..models import Album
from ...auth.auth_spotify import get_spotify_access_token


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
