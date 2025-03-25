import requests
from .spotify_auth import get_spotify_access_token
from .tidal_auth import get_tidal_access_token


async def convert_track_id(id: str) -> list[str]:
    streaming_links = await get_streaming_links(id)

    return streaming_links


async def get_isrc_code(id: str) -> int:
    platform = get_platform(id)
    isrc_code = 0
    if platform == "tidal":
        isrc_code = await get_isrc_tidal(id)
    elif platform == "spotify":
        isrc_code = await get_isrc_spotify(id)

    return isrc_code


async def get_isrc_tidal(tidal_id: str) -> int:
    # Example track link: tidal.com/browse/track/391366623?u
    access_token = get_tidal_access_token()
    if not access_token:
        print("Error getting access token")

    headers = {"Authorization": f"Bearer {access_token}"}
    request_url = f"https://openapi.tidal.com/v2/tracks/{tidal_id}?countryCode=GB"

    response = requests.get(request_url, headers=headers)
    respondeDecoded = response.json()

    return respondeDecoded["data"]["attributes"]["isrc"]


async def get_isrc_spotify(spotify_id: str) -> int:
    # Example track link: open.spotify.com/track/3tYxhPqkioZEV5el3DJxLQ?si=11c6f71d60184dac
    access_token = get_spotify_access_token()
    if not access_token:
        print("Error getting spotify access token")

    headers = {"Authorization": f"Bearer {access_token}"}
    request_url = f"https://api.spotify.com/v1/tracks/{spotify_id}"

    response = requests.get(request_url, headers=headers)
    response_decoded = response.json()

    return response_decoded["external_ids"]["isrc"]


def get_platform(id: str) -> str:
    # Tidal id format: 126102208
    # Spotify id format: 3tYxhPqkioZEV5el3DJxLQ
    if id.isnumeric():
        return "tidal"
    else:
        return "spotify"


async def get_streaming_links(id: str) -> list[str]:
    platform = get_platform(id)
    isrc_code = await get_isrc_code(id)
    streaming_links = []

    if platform == "spotify":
        streaming_links.append(await get_tidal_link(isrc_code))
    elif platform == "tidal":
        streaming_links.append(await get_spotify_link(isrc_code))

    return streaming_links


async def get_spotify_link(isrc: int) -> str:
    spotify_token = get_spotify_access_token()

    if not spotify_token:
        print("Error retrieving spotify access token")
        return "Not Found"

    headers = {"Authorization": f"Bearer {spotify_token}"}
    request_url = f"https://api.spotify.com/v1/search?q=isrc:{isrc}&type=track"
    response = requests.get(request_url, headers=headers)
    response_decoded = response.json()

    return response_decoded["tracks"]["items"][0]["external_urls"]["spotify"]


async def get_tidal_link(isrc: int) -> str:
    token = get_tidal_access_token()

    if not token:
        print("Error retrieving spotify access token")
        return "Not Found"

    headers = {"Authorization": f"Bearer {token}"}
    # request_url = f"https://api.spotify.com/v1/search?q=isrc:{isrc}&type=track"
    request_url = f"https://openapi.tidal.com/v2/tracks?countryCode=GB&include=albums&filter%5Bisrc%5D={isrc}&filter%5Bid%5D=251380837"
    response = requests.get(request_url, headers=headers)
    response_decoded = response.json()

    return response_decoded["data"][0]["attributes"]["externalLinks"][0]["href"]
