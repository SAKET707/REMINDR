from datetime import datetime, timedelta, timezone
# this file is for jwt and enxryption
from jose import jwt
from cryptography.fernet import Fernet
from core.config import settings

#create encryption object , used for google refresh token not JWT
# fernet uses symmetric encryption ie same secret key is used for both encryption n decryption
cipher = Fernet(settings.FERNET_KEY.encode())

# jwts dont live in db so no encryption to them.
# jwt is stateless ,stored by client in httponly cookie or localstorage but google refresh token is stored in backend 
# in fact if we store them they are signed so no tampering 
# if one know secret key then he can modify it

class Security:

    @staticmethod
    def create_access_token(user_id: int) -> str:
        # creates JWT with expiry time , payload then signs it . its never stored in db as jwts are stateless
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
            settings.SECRET_KEY, # secret key is for signing the jwts very dangerous if hacker gets it he can become any user 
            algorithm=settings.ALGORITHM,
        )

    @staticmethod # it checks signature matches secret key, token is not expired , and it has valid structure
    def verify_access_token(token: str) -> dict: # Raises JWTError if the token is invalid or expired.
        # decode , verify signature , verify expiry , return payload
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    
    @staticmethod
    def encrypt(text: str) -> str:
        # uses fernet to encrypt plain text to random cipher text for google refresh token before storing in postgresql
        return cipher.encrypt(text.encode()).decode()


    @staticmethod
    def decrypt(token: str) -> str:
        # uses fernet to decrypt random cipher text to plain text only when calling gmail apis
        return cipher.decrypt(token.encode()).decode()