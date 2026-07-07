from __future__ import annotations
from datetime import datetime, timezone
from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base
from typing import TYPE_CHECKING
from sqlalchemy import String

if TYPE_CHECKING:
    from models.email import Email
    from models.telegram_token import TelegramConnectToken

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    google_id: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    profile_picture: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    encrypted_refresh_token: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    telegram_chat_id: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    last_history_id: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    emails: Mapped[list["Email"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    telegram_connect_tokens: Mapped[list["TelegramConnectToken"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    gmail_watch_expiration: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )