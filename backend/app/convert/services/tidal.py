import requests
from ..exceptions import APIError
from ...auth.auth_tidal import get_tidal_access_token
from ..models import Album


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
