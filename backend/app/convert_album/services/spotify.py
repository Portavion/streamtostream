import requests
from ..exceptions import APIError
from ..models import Album
from ...auth.auth_spotify import get_spotify_access_token


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
