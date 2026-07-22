from fastapi import HTTPException, status
from sqlalchemy import func

from models.email import Email
from models.preparation_task import PreparationTask
from models.reminder import Reminder
from core.dependencies import Session

class PreparationTaskService:

    @staticmethod
    def get_all(
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

        return (
            db.query(PreparationTask)
            .filter(
                PreparationTask.reminder_id == reminder_id,
            )
            .order_by(PreparationTask.position)
            .all()
        )

    @staticmethod
    def get_all_for_user(
        db: Session,
        user_id: int,
    ):
        return (
            db.query(PreparationTask)
            .join(Reminder)
            .join(Email)
            .filter(
                Email.user_id == user_id,
            )
            .order_by(
                PreparationTask.reminder_id,
                PreparationTask.position,
            )
            .all()
        )

    @staticmethod
    def create(
        db,
        reminder_id,
        user_id,
        title,
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

        max_position = (
            db.query(func.max(PreparationTask.position))
            .filter(
                PreparationTask.reminder_id == reminder_id,
            )
            .scalar()
        )

        task = PreparationTask(
            reminder_id=reminder_id,
            title=title,
            completed=False,
            position=(max_position or 0) + 1,
        )

        db.add(task)
        db.commit()
        db.refresh(task)

        return task

    @staticmethod
    def update(
        db,
        task_id,
        user_id,
        title=None,
        completed=None,
    ):
        task = (
            db.query(PreparationTask)
            .join(Reminder)
            .join(Email)
            .filter(
                PreparationTask.id == task_id,
                Email.user_id == user_id,
            )
            .first()
        )

        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Preparation task not found.",
            )

        if title is not None:
            task.title = title

        if completed is not None:
            task.completed = completed

        db.commit()
        db.refresh(task)

        return task

    @staticmethod
    def delete(
        db,
        task_id,
        user_id,
    ):
        task = (
            db.query(PreparationTask)
            .join(Reminder)
            .join(Email)
            .filter(
                PreparationTask.id == task_id,
                Email.user_id == user_id,
            )
            .first()
        )

        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Preparation task not found.",
            )

        db.delete(task)
        db.commit()