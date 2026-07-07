from fastapi import APIRouter, Depends
from core.dependencies import get_db
from core.dependencies import get_current_user
from models.user import User
from sqlalchemy.orm import Session
from schemas.user_schema import UserResponse
from services.gmail_service import disable_gmail_watch

router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.get(
    "/me",
    response_model=UserResponse,
)
def me(
    current_user: User = Depends(get_current_user),
):
    return current_user




@router.delete("/account")
def delete_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    try:

        if current_user.encrypted_refresh_token:

            disable_gmail_watch(current_user)

    except Exception as e:

        print(f"Failed to stop Gmail watch: {e}")

    db.delete(current_user)

    db.commit()

    return {
        "message": "Account deleted successfully"
    }