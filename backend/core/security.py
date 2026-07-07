from datetime import datetime, timedelta, timezone

from jose import jwt
from cryptography.fernet import Fernet
from core.config import settings

cipher = Fernet(settings.FERNET_KEY.encode())

class Security:

    @staticmethod
    def create_access_token(user_id: int) -> str:

        expire = datetime.now(
            timezone.utc
        ) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload = {
            "user_id": user_id,
            "exp": expire,
        }

        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )

    @staticmethod
    def verify_access_token(token: str) -> dict:

        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    
    @staticmethod
    def encrypt(text: str) -> str:
        return cipher.encrypt(text.encode()).decode()


    @staticmethod
    def decrypt(token: str) -> str:
        return cipher.decrypt(token.encode()).decode()