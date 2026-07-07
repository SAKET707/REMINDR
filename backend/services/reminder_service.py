from datetime import datetime, timedelta, timezone

from models.reminder import Reminder
from sqlalchemy.orm import joinedload

from models.email import Email


class ReminderService:

    REMINDER_ADVANCE = timedelta(days=1)

    @staticmethod
    def create(
        db,
        email,
    ) -> Reminder:

        existing = (
            db.query(Reminder)
            .filter_by(email_id=email.id)
            .first()
        )

        if existing:
            return existing

        now = datetime.now(timezone.utc)

        # If the email has a deadline,
        # schedule the reminder 1 day before it.
        if email.deadline:

            scheduled_for = (
                email.deadline
                - ReminderService.REMINDER_ADVANCE
            )

            # If the reminder time has already passed,
            # notify the user soon instead.
            if scheduled_for <= now:
                scheduled_for = now + timedelta(minutes=5)

        # No deadline found.
        else:
            scheduled_for = now + timedelta(minutes=5)

        reminder = Reminder(
            email_id=email.id,
            scheduled_for=scheduled_for,
            status="PENDING",
        )

        db.add(reminder)
        db.flush()
        db.refresh(reminder)

        return reminder
    

    @staticmethod
    def get_due_reminders(db):

        now = datetime.now(timezone.utc)

        return (
            db.query(Reminder)
            .options(
                joinedload(Reminder.email)
                .joinedload(Email.user)
            )
            .filter(
                Reminder.status == "PENDING",
                Reminder.scheduled_for <= now,
            )
            .all()
        )