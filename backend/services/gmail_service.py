from google.oauth2.credentials import Credentials # it manages refresh token, expired access token, authorization header . google sdk
from googleapiclient.discovery import build # it creates a gmail client object that knows how to communicate with a google api
from datetime import datetime, UTC
import requests
from sqlalchemy.orm import Session
from core.security import Security
from core.config import settings
from models.user import User
from services.google_service import refresh_google_access_token

import logging
logger = logging.getLogger(__name__)

class GmailService:

    @staticmethod
    def build_service(refresh_token: str): # it outputs gmail client object made by build
        credentials = Credentials( # create an oauth credential object
            token=None, # we dont have a google access token yet
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            scopes=[
                "https://www.googleapis.com/auth/gmail.readonly" # only read gmails permision granted. principle of least privilege
            ],
        )

        return build(
            "gmail",
            "v1", # api version
            credentials=credentials,
            cache_discovery=False, #Google API has a discovery document that describes all available endpoints.
                                    # Older versions of the SDK cached it locally
                                    # that cache can create warnings or filesystem issues so false that
        )

    @staticmethod
    def get_message(service, message_id):
        return (
            service.users() # gmail api is organised by resources
            .messages()
            .get(
                userId="me", # since we already continue'd with google -> the oauth token tells that me = the authenticated user
                id=message_id,
                format="full", #bcos parserservice need to get subject sender body header. other option include minimal, metadata etc.
            )
            .execute() # triggers the request/contact 
        )

    @staticmethod
    def initial_sync(service, max_results=5): # if user sign in today then last_history_id = null in db so fetch latest 5(here) 
        logger.info("Starting initial Gmail sync")
        response = ( # this only gets id's and not bodies as they are huge
            service.users()
            .messages()
            .list(
                userId="me",
                maxResults=max_results,
            )
            .execute()
        )

        message_ids = response.get("messages", []) # in case mailbox empty response would be {} so to avoid keyerror crash .default is [] so loop runs 0 times

        emails = []

        latest_history_id = None

        for message in message_ids:

            email = GmailService.get_message(
                service,
                message["id"],
            )

            emails.append(email)

            latest_history_id = email["historyId"]
        logger.info(
            "Initial Gmail sync fetched %d email(s)",
            len(emails),
        )
        return {
            "emails": emails, # downloaded emails
            "latest_history_id": latest_history_id # latest history id
        }

    @staticmethod
    def incremental_sync(service, last_history_id): # this gets all changes after historyId = 'x' its fast and precise what we want
        logger.info(
            "Starting incremental Gmail sync from history_id=%s",
            last_history_id,
        )
        response = ( # asks what changed after historyId = 'x'
            service.users()
            .history()
            .list(
                userId="me",
                startHistoryId=last_history_id,
                historyTypes=["messageAdded"],# we care about new emails . labels change, arxhived, star added they dont need reminder again. principle of least work
            )
            .execute()
        )

        history = response.get("history", [])

        emails = []

        # Prevent processing the same Gmail message twice
        seen_message_ids = set()

        for record in history: # 1 record can contain many changes, like msgadded,msgdeleted,labeladded

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
        logger.info(
            "Incremental Gmail sync fetched %d new email(s)",
            len(emails),
        )
        return {
            "emails": emails,
            "latest_history_id": response.get(
                "historyId",
                last_history_id,
            ),
        }

    @staticmethod # other service call this they dont care whether initial or incremental 
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
    logger.info(
        "Enabling Gmail watch for user %s",
        current_user.email,
    )

    refresh_token = Security.decrypt(
        current_user.encrypted_refresh_token
    )

    access_token = refresh_google_access_token( # to authorize api request
        refresh_token
    )

    response = requests.post( 
        "https://gmail.googleapis.com/gmail/v1/users/me/watch", # gmail watch api .google creates a watch subscription for this mail
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        json={
            "topicName": settings.GMAIL_TOPIC, # google pub sub topic. google need to know where notifcn need to be published. that topic is configured inside google cloud
        },
    )

    response.raise_for_status()

    data = response.json() # google replies with a dict of historyId and expiration

    expiration = datetime.fromtimestamp(
        int(data["expiration"]) / 1000, # milliseconds to seconds becos py expects in seconds & google return in ms
        tz=UTC,
    )

    current_user.last_history_id = data["historyId"]
    current_user.gmail_watch_expiration = expiration

    db.flush() # this doesnt commit becos caller decides whether the whole transaction succeeded or not
    db.refresh(current_user) # load latest ORM state
    logger.info(
        "Gmail watch enabled for user %s",
        current_user.email,
    )
    return data



def disable_gmail_watch(current_user):
    logger.info(
        "Disabling Gmail watch for user %s",
        current_user.email,
    )
    refresh_token = Security.decrypt(
        current_user.encrypted_refresh_token
    )

    access_token = refresh_google_access_token(
        refresh_token
    )

    response = requests.post(
        "https://gmail.googleapis.com/gmail/v1/users/me/stop", # tells google to stop sending pub/sub notifications
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        timeout=15,
    )

    response.raise_for_status()
    logger.info(
        "Gmail watch disabled for user %s",
        current_user.email,
    )
    return response.json() if response.content else {}

