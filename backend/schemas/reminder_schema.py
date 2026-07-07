from datetime import datetime
from pydantic import BaseModel, ConfigDict

from schemas.email_schema import EmailSummaryResponse


class ReminderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    scheduled_for: datetime
    status: str
    sent_at: datetime | None

    email: EmailSummaryResponse