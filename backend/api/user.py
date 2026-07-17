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


@router.get( # return the currently logged in user
    "/me",
    response_model=UserResponse,
)
def me(
    current_user: User = Depends(get_current_user),
):
    return current_user # Fastapi automatically converts the SQLAlchemy model into the response schema using Pydantic becos of UserResponse
                        # filtering out fields that shouldnt be exposed



@router.delete("/account") # here delete the user's account
def delete_account(
    db: Session = Depends(get_db), # we need db session to delete the row
    current_user: User = Depends(get_current_user), # delete the logged in users account
):

    try:

        if current_user.encrypted_refresh_token: # stop gmail watch first.

            disable_gmail_watch(current_user)

    except Exception as e:

        print(f"Failed to stop Gmail watch: {e}")

    db.delete(current_user) # only mark the object for deleteion

    db.commit()

    return {
        "message": "Account deleted successfully"
    }