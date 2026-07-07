import requests

from config import BACKEND_URL


def verify_telegram(token: str, chat_id: str):
    response = requests.post(
        f"{BACKEND_URL}/telegram/verify",
        json={
            "token": token,
            "chat_id": chat_id,
        },
    )

    return response