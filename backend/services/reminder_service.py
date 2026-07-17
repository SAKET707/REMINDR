from datetime import datetime, timedelta, timezone

from models.reminder import Reminder
from sqlalchemy.orm import joinedload
# this decides when should the user be reminded
from models.email import Email


class ReminderService:

    ONE_DAY = timedelta(days=1)
    FOUR_HOURS = timedelta(hours=4)
    ONE_HOUR = timedelta(hours=1)

    @staticmethod
    def create(
        db,
        email, # this email ORM object contains already all reqd info
    ) -> Reminder:

        existing = (
            db.query(Reminder)
            .filter_by(email_id=email.id)
            .first()
        )

        if existing: # again duplicate check no need to create 2 identical reminders for 1 mail
            return existing

        now = datetime.now(timezone.utc)

        # If the email has a deadline,
        # schedule the reminder according to this logic 
        if email.deadline:
            time_until_deadline = email.deadline - now

            if time_until_deadline > ReminderService.ONE_DAY:
                scheduled_for = email.deadline - ReminderService.ONE_DAY

            elif time_until_deadline > timedelta(hours=12):
                scheduled_for = email.deadline - ReminderService.FOUR_HOURS

            elif time_until_deadline > timedelta(hours=4):
                scheduled_for = email.deadline - ReminderService.ONE_HOUR

            else:
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
    def get_due_reminders(db): # this is used by scheduler 

        now = datetime.now(timezone.utc)
 
        return ( # here n+1 query problem . will learn
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