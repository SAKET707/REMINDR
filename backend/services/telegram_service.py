import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from models.telegram_token import TelegramConnectToken
from models.user import User

from datetime import datetime, timezone

from models.telegram_token import TelegramConnectToken

def create_connect_token(
    db: Session,
    current_user: User,
) -> str:

    # Remove any existing unused connect tokens for this user
    db.query(TelegramConnectToken).filter(
        TelegramConnectToken.user_id == current_user.id
    ).delete()

    # Generate a new secure token
    token = secrets.token_urlsafe(32)

    connect_token = TelegramConnectToken(
        user_id=current_user.id,
        token=token,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
    )

    db.add(connect_token)

    # Commit delete + insert together
    db.commit()

    return token





def verify_telegram_connection(
    db: Session,
    token: str,
    chat_id: str,
) -> bool:

    connect_token = (
        db.query(TelegramConnectToken)
        .filter(TelegramConnectToken.token == token)
        .first()
    )

    if connect_token is None:
        return False

    if connect_token.expires_at < datetime.now(timezone.utc):
        db.delete(connect_token)
        db.commit()
        return False

    user = (
        db.query(User)
        .filter(User.id == connect_token.user_id)
        .first()
    )

    if user is None:
        return False

    user.telegram_chat_id = chat_id

    db.delete(connect_token)

    db.commit()

    return True