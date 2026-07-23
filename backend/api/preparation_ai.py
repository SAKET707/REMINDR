from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from agents.preparation_agent import PreparationAgent
from core.dependencies import get_db
from core.dependencies import get_current_user
from services.preparation_ai_service import PreparationAIService
from models.reminder import Reminder
from models.email import Email



router = APIRouter(
    prefix="/preparation-ai",
    tags=["Preparation AI"],
)


@router.post("/reminder/{reminder_id}/generate")
def generate_preparation_tasks(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    reminder = (
        db.query(Reminder)
        .join(Reminder.email)
        .filter(
            Reminder.id == reminder_id,
            Email.user_id == current_user.id,
        )
        .first()
    )

    if reminder is None:
        raise HTTPException(
            status_code=404,
            detail="Reminder not found.",
        )

    suggestions = PreparationAIService.generate(
        db=db,
        reminder_id=reminder.id,
        subject=reminder.email.subject,
        summary=reminder.email.summary,
        deadline=reminder.email.deadline,
    )

    return {
        "suggestions": suggestions,
    }