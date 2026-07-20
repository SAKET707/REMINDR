import json
from datetime import datetime, timezone

from models.email import Email
from models.reminder import Reminder



TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_user_reminders",
            "description": (
                "Returns all upcoming reminders for the user. "
                "Call this function only once if existing reminders are needed. "
                "The returned data contains everything required to make the scheduling decision. "
                "Do not call this function again after receiving its result."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The user's id."
                    }
                },
                "required": ["user_id"],
            },
        },
    }
]


def get_user_reminders(db, user_id: int) -> str:
    """
    Returns upcoming reminders as JSON.

    This function is exposed to the SchedulingAgent.
    """

    now = datetime.now(timezone.utc)

    reminders = (
        db.query(Reminder)
        .join(Reminder.email)
        .filter(
            Email.user_id == user_id,
            Reminder.status == "PENDING",
            Reminder.scheduled_for >= now,
        )
        .order_by(Reminder.scheduled_for)
        .all()
    )

    result = [
        {
            "scheduled_for": reminder.scheduled_for.isoformat(),
            "summary": reminder.email.summary,
            "deadline": (
                reminder.email.deadline.isoformat()
                if reminder.email.deadline
                else None
            ),
        }
        for reminder in reminders
    ]

    return json.dumps(result)

AVAILABLE_TOOLS = {
    "get_user_reminders": get_user_reminders,
}