from pydantic import BaseModel


class TelegramConnectResponse(BaseModel):
    token: str


class TelegramVerifyRequest(BaseModel):
    token: str
    chat_id: str