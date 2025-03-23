import requests
import base64
from dotenv import load_dotenv
import os

load_dotenv()


def get_spotify_access_token():
    try:
        creds = f"{os.getenv('SPOTIFY_CLIENT_ID')}:{os.getenv('SPOTIFY_CLIENT_SECRET')}"
        creds_bytes = creds.encode("ascii")
        creds_base64 = base64.b64encode(creds_bytes).decode("ascii")
        token_url = "https://accounts.spotify.com/api/token"

        headers = {
            "Authorization": f"Basic {creds_base64}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "client_credentials",
        }

        response = requests.post(token_url, headers=headers, data=data)
        response.raise_for_status()

        token_data = response.json()
        access_token = token_data.get("access_token")

        return access_token

    except requests.exceptions.RequestException as e:
        print(f"Error getting Spotify access token: {e}")
        return None
    except ValueError as e:
        print(f"Error decoding JSON: {e}")
        return None
    except KeyError as e:
        print(f"Key error in JSON: {e}")
        return None
