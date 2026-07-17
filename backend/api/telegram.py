from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from core.dependencies import get_current_user, get_db
from models.user import User

from schemas.telegram_schema import (
    TelegramConnectResponse,
    TelegramVerifyRequest,
)

from services.telegram_service import (
    create_connect_token, # defines the response for /connect
    verify_telegram_connection, # validates the incoming json for /verify
)

router = APIRouter(
    prefix="/telegram",
    tags=["Telegram"],
)


@router.post(
    "/connect",
    response_model=TelegramConnectResponse,
)
def connect_telegram( # Generate a temporary secure token that links the current user to a Telegram chat as Exposing user IDs would be less secure and easier to misuse
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    token = create_connect_token(
        db=db,
        current_user=current_user,
    )

    return TelegramConnectResponse(
        token=token,
    )


@router.post("/verify")
def verify_telegram( # This verifies that the token received from Telegram
    request: TelegramVerifyRequest,
    db: Session = Depends(get_db),
):

    success = verify_telegram_connection(
        db=db,
        token=request.token,
        chat_id=request.chat_id,
    )

    if not success:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired token",
        )

    return {
        "message": "Telegram connected successfully."
    }