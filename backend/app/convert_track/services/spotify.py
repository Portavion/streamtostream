import requests
from ..exceptions import APIError
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
