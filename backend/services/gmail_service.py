from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, UTC
import requests

from sqlalchemy.orm import Session

from core.security import Security
from core.config import settings
from models.user import User

from services.google_service import refresh_google_access_token


class GmailService:

    @staticmethod
    def build_service(refresh_token: str):
        credentials = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            scopes=[
                "https://www.googleapis.com/auth/gmail.readonly"
            ],
        )

        return build(
            "gmail",
            "v1",
            credentials=credentials,
            cache_discovery=False,
        )

    @staticmethod
    def get_message(service, message_id):
        return (
            service.users()
            .messages()
            .get(
                userId="me",
                id=message_id,
                format="full",
            )
            .execute()
        )

    @staticmethod
    def initial_sync(service, max_results=5):

        response = (
            service.users()
            .messages()
            .list(
                userId="me",
                maxResults=max_results,
            )
            .execute()
        )

        message_ids = response.get("messages", [])

        emails = []

        latest_history_id = None

        for message in message_ids:

            email = GmailService.get_message(
                service,
                message["id"],
            )

            emails.append(email)

            latest_history_id = email["historyId"]

        return {
            "emails": emails,
            "latest_history_id": latest_history_id
        }

    @staticmethod
    def incremental_sync(service, last_history_id):

        response = (
            service.users()
            .history()
            .list(
                userId="me",
                startHistoryId=last_history_id,
                historyTypes=["messageAdded"],
            )
            .execute()
        )

        history = response.get("history", [])

        emails = []

        # Prevent processing the same Gmail message twice
        seen_message_ids = set()

        for record in history:

            for item in record.get("messagesAdded", []):

                message_id = item["message"]["id"]

                if message_id in seen_message_ids:
                    continue

                seen_message_ids.add(message_id)

                email = GmailService.get_message(
                    service,
                    message_id,
                )

                emails.append(email)

        return {
            "emails": emails,
            "latest_history_id": response.get(
                "historyId",
                last_history_id,
            ),
        }

    @staticmethod
    def sync(refresh_token, last_history_id):

        service = GmailService.build_service(refresh_token)

        if last_history_id is None:

            return GmailService.initial_sync(
                service,
                max_results=5,
            )

        return GmailService.incremental_sync(
            service,
            last_history_id,
        )
    

def enable_gmail_watch(
    db: Session,
    current_user: User,
):

    refresh_token = Security.decrypt(
        current_user.encrypted_refresh_token
    )

    access_token = refresh_google_access_token(
        refresh_token
    )

    response = requests.post(
        "https://gmail.googleapis.com/gmail/v1/users/me/watch",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        json={
            "topicName": settings.GMAIL_TOPIC,
        },
    )

    response.raise_for_status()

    data = response.json()

    expiration = datetime.fromtimestamp(
        int(data["expiration"]) / 1000,
        tz=UTC,
    )

    current_user.last_history_id = data["historyId"]
    current_user.gmail_watch_expiration = expiration

    db.flush()
    db.refresh(current_user)

    return data



def disable_gmail_watch(current_user):

    refresh_token = Security.decrypt(
        current_user.encrypted_refresh_token
    )

    access_token = refresh_google_access_token(
        refresh_token
    )

    response = requests.post(
        "https://gmail.googleapis.com/gmail/v1/users/me/stop",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        timeout=15,
    )

    response.raise_for_status()

    return response.json() if response.content else {}

