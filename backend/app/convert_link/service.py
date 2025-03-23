import requests
from .spotify_auth import get_spotify_access_token
from .tidal_auth import get_tidal_access_token


async def convert_track_link(request_link: str) -> list[str]:
    streaming_links = await get_streaming_links(request_link)

    return streaming_links


async def get_isrc_code(link: str) -> int:
    platform = get_platform(link)
    isrc_code = 0
    if platform == "tidal":
        isrc_code = await get_isrc_tidal(link)
    elif platform == "spotify":
        isrc_code = await get_isrc_spotify(link)

    return isrc_code


async def get_isrc_tidal(link: str) -> int:
    # Example track link: tidal.com/browse/track/391366623?u
    track_id = link.split("/")[-1]
    track_id = track_id.strip("?u")

    access_token = get_tidal_access_token()
    if not access_token:
        print("Error getting access token")

    headers = {"Authorization": f"Bearer {access_token}"}
    request_url = f"https://openapi.tidal.com/v2/tracks/{track_id}?countryCode=GB"

    response = requests.get(request_url, headers=headers)
    respondeDecoded = response.json()

    return respondeDecoded["data"]["attributes"]["isrc"]


async def get_isrc_spotify(link: str) -> int:
    # Example track link: open.spotify.com/track/3tYxhPqkioZEV5el3DJxLQ?si=11c6f71d60184dac
    track_id = link.split("/track/")[-1]
    track_id = track_id.split("?")[0]

    access_token = get_spotify_access_token()
    if not access_token:
        print("Error getting spotify access token")

    headers = {"Authorization": f"Bearer {access_token}"}
    request_url = f"https://api.spotify.com/v1/tracks/{track_id}"

    response = requests.get(request_url, headers=headers)
    response_decoded = response.json()

    return response_decoded["external_ids"]["isrc"]


def get_platform(link: str) -> str:
    if "spotify" in link:
        return "spotify"
    elif "tidal" in link:
        return "tidal"
    else:
        return "not found"


async def get_streaming_links(link: str) -> list[str]:
    platform = get_platform(link)
    isrc_code = await get_isrc_code(link)
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


def extract_track_id(link: str) -> int:
    track_id = link.split("/")[-1]
    track_id = track_id.strip("?u")

    return int(track_id)
