import requests
import base64
from dotenv import load_dotenv
import os

load_dotenv()


def get_tidal_access_token():
    try:
        creds = f"{os.getenv('TIDAL_CLIENT_ID')}:{os.getenv('TIDAL_CLIENT_SECRET')}"
        creds_bytes = creds.encode("ascii")
        creds_b64 = base64.b64encode(creds_bytes).decode("ascii")

        # Set the request headers
        headers = {
            "Authorization": f"Basic {creds_b64}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        # Set the request data
        data = {"grant_type": "client_credentials"}

        # Make the POST request
        response = requests.post(
            "https://auth.tidal.com/v1/oauth2/token", headers=headers, data=data
        )

        # Check the response status code
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        # Parse the JSON response
        token_data = response.json()

        # Extract the access token
        access_token = token_data.get("access_token")
        return access_token

    except requests.exceptions.RequestException as e:
        print(f"Error getting Tidal access token: {e}")
        return None
    except ValueError as e:
        print(f"Error decoding JSON: {e}")
        return None
    except KeyError as e:
        print(f"Key error in JSON: {e}")
        return None
