from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from core.dependencies import get_db
from services import oauth_service

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.get("/google/login")
async def login(request: Request):
    return await oauth_service.google_login(request)

@router.get("/google/callback", name="google_callback")
async def google_callback(
    request: Request,
    db: Session = Depends(get_db),
):
    return await oauth_service.google_callback(
        request,
        db,
    )