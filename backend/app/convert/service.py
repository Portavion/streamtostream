import requests
from .auth_spotify import get_spotify_access_token
from .auth_tidal import get_tidal_access_token
from pydantic import BaseModel


class Album(BaseModel):
    artist: str
    album_name: str
    release_date: str
    upc: str


async def convert_track_id(id: str) -> list[str]:
    """Convert a track id to a list of links for other various streaming platforms (supports: Spotify and Tidal)"""
    return await get_track_streaming_links(id)


async def convert_album_id(id: str) -> list[str]:
    """Convert an album id to a list of links for other various streaming platforms (supports: Spotify and Tidal)"""
    return await get_album_links(id)


def get_platform(id: str) -> str:
    # Tidal id format: 126102208
    # Spotify id format: 3tYxhPqkioZEV5el3DJxLQ
    if id.isnumeric():
        return "tidal"
    else:
        return "spotify"


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


async def get_track_streaming_links(id: str) -> list[str]:
    platform = get_platform(id)
    isrc_code = await get_isrc_code(id)
    streaming_links = []

    if platform == "spotify":
        streaming_links.append(await get_tidal_track_link(isrc_code))
    elif platform == "tidal":
        streaming_links.append(await get_spotify_track_link(isrc_code))

    return streaming_links


async def get_spotify_track_link(isrc: int) -> str:
    spotify_token = get_spotify_access_token()

    if not spotify_token:
        print("Error retrieving spotify access token")
        return "Not Found"

    headers = {"Authorization": f"Bearer {spotify_token}"}
    request_url = f"https://api.spotify.com/v1/search?q=isrc:{isrc}&type=track"
    response = requests.get(request_url, headers=headers)
    response_decoded = response.json()

    return response_decoded["tracks"]["items"][0]["external_urls"]["spotify"]


async def get_tidal_track_link(isrc: int) -> str:
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


async def get_album_links(id: str) -> list[str]:
    platform = get_platform(id)
    album_info = await get_album_info(id)
    streaming_links = []

    if platform == "spotify":
        streaming_links.append(await get_tidal_album_link(album_info))
        pass
    elif platform == "tidal":
        streaming_links.append(await get_spotify_album_link(album_info))
        pass

    return streaming_links


async def get_album_info(id: str) -> Album:
    platform = get_platform(id)
    album_info = Album(
        **{"artist": "", "album_name": "", "release_date": "", "upc": ""}
    )
    if platform == "tidal":
        album_info = await get_album_info_tidal(id)
    elif platform == "spotify":
        album_info = await get_album_info_spotify(id)

    return album_info


async def get_album_info_tidal(tidal_id: str) -> Album:
    # Example query https://openapi.tidal.com/v2/albums/126102201?countryCode=US&include=artists

    access_token = get_tidal_access_token()
    if not access_token:
        print("Error getting access token")

    headers = {"Authorization": f"Bearer {access_token}"}
    request_url = (
        f"https://openapi.tidal.com/v2/albums/{tidal_id}?countryCode=GB&include=artists"
    )

    response = requests.get(request_url, headers=headers)
    responseDecoded = response.json()
    album_title = responseDecoded["data"]["attributes"]["title"]
    album_release_date = responseDecoded["data"]["attributes"]["releaseDate"]
    album_artist = responseDecoded["included"][0]["attributes"]["name"]
    album_upc = responseDecoded["data"]["attributes"]["barcodeId"]

    return Album(
        **{
            "artist": album_artist,
            "album_name": album_title,
            "release_date": album_release_date,
            "upc": album_upc,
        }
    )


async def get_album_info_spotify(spotify_id: str) -> Album:
    # Example query https://api.spotify.com/v1/albums/4aawyAB9vmqN3uQ7FjRGTy

    access_token = get_spotify_access_token()
    if not access_token:
        print("Error getting access token")

    headers = {"Authorization": f"Bearer {access_token}"}
    request_url = f"https://api.spotify.com/v1/albums/{spotify_id}"

    response = requests.get(request_url, headers=headers)
    responseDecoded = response.json()
    album_title = responseDecoded["name"]
    album_release_date = responseDecoded["release_date"]
    album_artist = responseDecoded["artists"][0]["name"]
    album_upc = responseDecoded["external_ids"]["upc"]

    return Album(
        **{
            "artist": album_artist,
            "album_name": album_title,
            "release_date": album_release_date,
            "upc": album_upc,
        }
    )


async def get_tidal_album_link(album_info: Album) -> str:
    token = get_tidal_access_token()

    if not token:
        print("Error retrieving spotify access token")
        return "Not Found"

    headers = {"Authorization": f"Bearer {token}"}
    # Example query: https://openapi.tidal.com/v2/albums?countryCode=GM&include=artists&include=items&filter%5BbarcodeId%5D=196589525444
    request_url = f"https://openapi.tidal.com/v2/albums?countryCode=GM&include=artists&include=items&filter%5BbarcodeId%5D={album_info.upc}"
    response = requests.get(request_url, headers=headers)
    response_decoded = response.json()

    return response_decoded["data"][0]["attributes"]["externalLinks"][0]["href"]


async def get_spotify_album_link(album_info: Album) -> str:
    token = get_spotify_access_token()

    if not token:
        print("Error retrieving spotify access token")
        return "Not Found"

    headers = {"Authorization": f"Bearer {token}"}
    # Example query: https://api.spotify.com/v1/search?q=upc%3A811774020510&type=album
    request_url = (
        f"https://api.spotify.com/v1/search?q=upc%3A{album_info.upc}&type=album"
    )
    response = requests.get(request_url, headers=headers)
    response_decoded = response.json()

    return response_decoded["albums"]["items"][0]["external_urls"]["spotify"]
