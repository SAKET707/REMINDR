import requests

from core.config import settings


def refresh_google_access_token(refresh_token: str) -> str:

    response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        },
    )

    response.raise_for_status()

    return response.json()["access_token"]