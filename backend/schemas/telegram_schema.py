from pydantic import BaseModel


class TelegramConnectResponse(BaseModel):
    token: str


class TelegramVerifyRequest(BaseModel): # backend expects these 2 and Validates incoming JSON before it reaches the service layer.
    token: str
    chat_id: str