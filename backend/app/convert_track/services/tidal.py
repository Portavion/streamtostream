import requests
from ..exceptions import APIError
from ...auth.auth_tidal import get_tidal_access_token


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
