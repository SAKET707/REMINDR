from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import get_db, get_current_user
from models.user import User
from services.sync_service import SyncService

router = APIRouter(
    prefix="/sync",
    tags=["Sync"],
)


@router.post("/") # post becos it changes server state, it fetches mails, change db , so not readonly operations
def sync(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    SyncService.sync_user(
        db=db,
        user=current_user,
    )

    return {
        "message": "Sync completed successfully."
    }