from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
# APIRouter groups related endpoints , so easy to maintain
from core.dependencies import get_db
from services import oauth_service

router = APIRouter( 
    prefix="/auth", # so /google/login becomes auth/google/login
    tags=["Authentication"] # instead of default , it becomes authentication in swagger
)


@router.get("/google/login") # it doesnt modify db but only redirects browser to google. authorization code is returned as query parameters in a GET request
async def login(request: Request):
    return await oauth_service.google_login(request)

@router.get("/google/callback", name="google_callback") # google redirects here after login
async def google_callback(
    request: Request,
    db: Session = Depends(get_db), # callback creates, updates user, store refresh token so session created
):
    return await oauth_service.google_callback(
        request,
        db,
    )