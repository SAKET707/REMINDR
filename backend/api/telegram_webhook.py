from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
# this is used by telegram server not by frontend
from core.dependencies import get_db
from services.telegram_service import verify_telegram_connection
from services.tele_noti_service import TeleNotiService

router = APIRouter(
    prefix="/telegram",
    tags=["Telegram"],
)


@router.post("/webhook") # Telegram calls this URL whenever a user sends a message to your bot
async def telegram_webhook( 
    request: Request,
    db: Session = Depends(get_db),
):

    update = await request.json()

    message = update.get("message")

    if message is None:
        return {"ok": True}

    chat_id = str(message["chat"]["id"])

    text = message.get("text", "")

    if not text.startswith("/start"):

        TeleNotiService.send_message(
            chat_id,
            "Unknown command.",
        )

        return {"ok": True}

    parts = text.split(maxsplit=1)

    if len(parts) == 1:

        reply = (
            "👋 Welcome to REMINDR!\n\n"
            "Please connect your account from the REMINDR website."
        )

    else:

        token = parts[1]

        success = verify_telegram_connection(
            db=db,
            token=token,
            chat_id=chat_id,
        )

        if success:

            reply = (
                "✅ Telegram connected successfully!\n\n"
                "You'll now receive REMINDR notifications here."
            )

        else:

            reply = (
                "❌ Invalid or expired connection link.\n"
                "Please connect again from REMINDR."
            )

    TeleNotiService.send_message(
        chat_id,
        reply,
    )

    return {"ok": True}
