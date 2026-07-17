from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import get_current_user, get_db
from models.user import User

from services.gmail_service import enable_gmail_watch
from services.sync_service import SyncService
import base64
import json
from fastapi import Request
from services.user_service import get_user_by_email

router = APIRouter(
    prefix="/gmail",
    tags=["Gmail"],
)


@router.post("/watch") # Enable Gmail Push Notifications for the authenticated user.
def gmail_watch(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    data = enable_gmail_watch(
    db=db,
    current_user=current_user,
)

    db.commit()

    return data




@router.post("/webhook") # Google Pub/Sub calls it automatically.
async def gmail_webhook(
    request: Request,
    db: Session = Depends(get_db),
):

    body = await request.json()

    encoded = body["message"]["data"]

    decoded = base64.b64decode(encoded).decode()

    payload = json.loads(decoded)

    user = get_user_by_email(
        db=db,
        email=payload["emailAddress"],
    )
    SyncService.sync_user(
        db=db,
        user=user,
    )

    return {"status": "ok"}

    