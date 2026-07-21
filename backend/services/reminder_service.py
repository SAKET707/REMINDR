from datetime import datetime, timezone
from fastapi import HTTPException, status
from agents.scheduling_agent import SchedulingAgent
from models.email import Email
from models.reminder import Reminder
from sqlalchemy.orm import joinedload

import logging
logger = logging.getLogger(__name__)


class ReminderService:

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
            logger.debug(
                "Reminder already exists for email_id=%d",
                email.id,
            )
            return existing

        scheduled_for = SchedulingAgent.run(
            db=db,
            email=email,
        )

        now = datetime.now(timezone.utc)

        if scheduled_for <= now:
            raise ValueError(
                "Scheduling agent returned a reminder in the past."
            )

        if (
            email.deadline is not None
            and scheduled_for >= email.deadline
        ):
            raise ValueError(
                "Scheduling agent returned a reminder after the deadline."
            )

        reminder = Reminder(
            email_id=email.id,
            scheduled_for=scheduled_for,
            status="PENDING",
        )

        db.add(reminder)
        db.flush()
        db.refresh(reminder)

        logger.info(
            "Created reminder id=%d for email_id=%d scheduled_for=%s",
            reminder.id,
            email.id,
            scheduled_for.isoformat(),
        )

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
    
    @staticmethod
    def update(
        db,
        reminder_id,
        user_id,
        scheduled_for,
    ):
        reminder = (
            db.query(Reminder)
            .join(Email)
            .filter(
                Reminder.id == reminder_id,
                Email.user_id == user_id,
            )
            .first()
        )

        if reminder is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reminder not found.",
            )

        if reminder.status != "PENDING":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pending reminders can be updated.",
            )

        now = datetime.now(timezone.utc)

        if scheduled_for <= now:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reminder time must be in the future.",
            )

        if (
            reminder.email.deadline is not None
            and scheduled_for >= reminder.email.deadline
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reminder must be before the deadline.",
            )

        reminder.scheduled_for = scheduled_for

        db.commit()
        db.refresh(reminder)

        logger.info(
            "Updated reminder id=%d scheduled_for=%s",
            reminder.id,
            reminder.scheduled_for.isoformat(),
        )

        return reminder
    
    @staticmethod
    def delete(
        db,
        reminder_id,
        user_id,
    ):
        reminder = (
            db.query(Reminder)
            .join(Email)
            .filter(
                Reminder.id == reminder_id,
                Email.user_id == user_id,
            )
            .first()
        )

        if reminder is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reminder not found.",
            )

        if reminder.status != "PENDING":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pending reminders can be deleted.",
            )

        db.delete(reminder.email)

        db.commit()

        logger.info(
            "Deleted reminder id=%d for user id=%d",
            reminder_id,
            user_id,
        )