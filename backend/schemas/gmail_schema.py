from pydantic import BaseModel


class GmailWatchResponse(BaseModel):
    history_id: str
    expiration: int