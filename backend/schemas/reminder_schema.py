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
         # Nested schema.
        # Instead of returning only email_id, the API returns
        # selected email details in the same response.
            #  no extra api request needed