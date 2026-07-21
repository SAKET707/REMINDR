from fastapi import Request
from fastapi.responses import RedirectResponse
from core.oauth import oauth
from sqlalchemy.orm import Session
from core.config import settings
from services.user_service import create_or_update_google_user
from core.security import Security
from services.gmail_service import enable_gmail_watch
from datetime import datetime,timezone

import logging
logger = logging.getLogger(__name__)

async def google_login(request: Request): # simply redirect the user to google login page
    redirect_uri = request.url_for("google_callback")

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri,
        access_type="offline", # google normally gives access token but with this it also gives refresh token
        prompt="consent", # Google may not issue a refresh token if the user has already granted consent before
                          # forces the consent screen to appear again, allowing Google to issue a new refresh token
    )


async def google_callback(
    request: Request,
    db: Session,
):
    token = await oauth.google.authorize_access_token(request)

    userinfo = token["userinfo"]
    logger.info(
        "Google OAuth successful for %s",
        userinfo["email"],
    )
    user = create_or_update_google_user(
        db=db,
        google_id=userinfo["sub"], # sub never changes.it is permanant unique identifier, emails can change
        email=userinfo["email"],
        name=userinfo["name"],
        profile_picture=userinfo.get("picture"),
        refresh_token=(
            Security.encrypt(token["refresh_token"])
            if token.get("refresh_token")
            else None
        ),
    )

    needs_watch = (
        user.last_history_id is None # new user , never synced
        or user.gmail_watch_expiration is None # no active watch
        or user.gmail_watch_expiration <= datetime.now(timezone.utc) # watch expired renew it
    )

    if needs_watch:

        try:

            enable_gmail_watch(
                db=db,
                current_user=user,
            )

            db.commit()

        except Exception:

            db.rollback()

            logger.exception(
                "Failed to enable Gmail watch for %s",
                user.email,
            )

    access_token = Security.create_access_token(user.id) # Google OAuth is only used for login and identity verification.
                                                        # After that, our backend issues its own JWT, which is used for stateless authentication between the frontend and backend
    frontend_url = settings.FRONTEND_URL

    logger.info(
        "User %s logged in successfully",
        user.email,
    )

    frontend_url = settings.FRONTEND_URL.rstrip("/")

    return RedirectResponse(
        url=f"{frontend_url}/oauth/callback?token={access_token}"
    )