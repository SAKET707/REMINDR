import requests # google oauth servers exposes an http api

from core.config import settings
# get a new access token using refresh token instead of asking user to sign in again

def refresh_google_access_token(refresh_token: str) -> str:

    response = requests.post( # token endpoint is defined as POST /token
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": settings.GOOGLE_CLIENT_ID, # tells google oauth server that this req is made by remindr out of million apps
            "client_secret": settings.GOOGLE_CLIENT_SECRET, # this proves that this app is really remindr to prevent attacks as client id are public
            "refresh_token": refresh_token,
            "grant_type": "refresh_token", # out of many grant types like authorisation code, this tells that session is being refreshed
        },
    )

    response.raise_for_status()

    return response.json()["access_token"]
