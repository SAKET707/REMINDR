from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import get_db, get_current_user
from models.email import Email
from models.user import User

router = APIRouter(
    prefix="/emails",
    tags=["Emails"],
)


@router.get("/") # returns all emails belonging to the loggedin user
def get_emails(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    emails = (
        db.query(Email)
        .filter(
            Email.user_id == current_user.id
        )
        .order_by(
            Email.received_at.desc()
        )
        .all()
    )

    return emails