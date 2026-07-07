from fastapi import Request
from fastapi.responses import RedirectResponse
from core.oauth import oauth
from sqlalchemy.orm import Session
from core.config import settings
from services.user_service import create_or_update_google_user
from core.security import Security
from services.gmail_service import enable_gmail_watch
from datetime import datetime,timezone

async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri,
        access_type="offline",
        prompt="consent",
    )


async def google_callback(
    request: Request,
    db: Session,
):
    token = await oauth.google.authorize_access_token(request)

    userinfo = token["userinfo"]

    user = create_or_update_google_user(
        db=db,
        google_id=userinfo["sub"],
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
        user.last_history_id is None
        or user.gmail_watch_expiration is None
        or user.gmail_watch_expiration <= datetime.now(timezone.utc)
    )

    if needs_watch:

        try:

            enable_gmail_watch(
                db=db,
                current_user=user,
            )

            db.commit()

        except Exception as e:

            db.rollback()

            print(
                f"Failed to enable Gmail Watch: {e}"
            )

    access_token = Security.create_access_token(user.id)
    frontend_url = settings.FRONTEND_URL

    return RedirectResponse(
        url=f"{frontend_url}/oauth/callback?token={access_token}"
    )