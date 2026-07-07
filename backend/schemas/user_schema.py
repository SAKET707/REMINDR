from pydantic import BaseModel, ConfigDict

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    profile_picture: str | None
    telegram_chat_id: str | None

    model_config = ConfigDict(
        from_attributes=True
    )