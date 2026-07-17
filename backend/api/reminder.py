from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from core.dependencies import get_db, get_current_user
from models.reminder import Reminder
from models.email import Email
from models.user import User
from schemas.reminder_schema import ReminderResponse
from services.reminder_service import ReminderService

router = APIRouter(
    prefix="/reminders",
    tags=["Reminders"],
)


@router.get(
    "/",
    response_model=list[ReminderResponse],
)
def get_reminders( # returns a list of reminders for the authenticated user
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    reminders = (
        db.query(Reminder)
        .options(joinedload(Reminder.email))
        .join(Email)
        .filter(Email.user_id == current_user.id)
        .all()
    )

    return reminders

@router.get("/test-reminders") # this is for testing
def test_reminders(
    db: Session = Depends(get_db),
):
    reminders = ReminderService.get_due_reminders(db)

    return {
        "count": len(reminders),
    }