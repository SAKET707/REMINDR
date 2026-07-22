from fastapi import FastAPI
from api.auth import router as auth_router
from starlette.middleware.sessions import SessionMiddleware
from core.config import settings
from models import User, Email, Reminder
from api import sync
from api import email,reminder,user
from fastapi.middleware.cors import CORSMiddleware
from api import telegram
from api import gmail
from contextlib import asynccontextmanager
from services.scheduler_service import start_scheduler, scheduler
from core.config import settings
from api import telegram_webhook
import logging
from core.logging_config import setup_logging
from api.preparation_task import router as preparation_task_router

setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Starting REMINDR scheduler...")
    start_scheduler()

    yield

    logger.info("Stopping REMINDR scheduler...")
    scheduler.shutdown()


app = FastAPI(
    title="REMINDR API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        settings.FRONTEND_URL,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sync.router)
app.include_router(auth_router)
app.include_router(email.router)
app.include_router(reminder.router)
app.include_router(user.router)
app.include_router(telegram.router)
app.include_router(gmail.router)
app.include_router(telegram_webhook.router)
app.include_router(preparation_task_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to REMINDR API"
    }
