from pydantic import BaseModel, ConfigDict

# Response schema.
# Only exposes fields safe for the frontend.
# Internal/sensitive fields like google_id, refresh token,
# history_id etc. are intentionally omitted.
class UserResponse(BaseModel): # here we filetered what we needed like we avoid google_id or refresh token as it is sensitive
    id: int
    name: str
    email: str
    profile_picture: str | None
    telegram_chat_id: str | None

    model_config = ConfigDict(
        from_attributes=True
    )