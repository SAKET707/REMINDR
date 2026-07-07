from pydantic import BaseModel, ConfigDict


class EmailSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sender: str
    subject: str
    summary: str