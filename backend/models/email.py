from __future__ import annotations
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base

if TYPE_CHECKING:
    from models.user import User
    from models.reminder import Reminder


class Email(Base):
    __tablename__ = "emails"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    gmail_message_id: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    thread_id: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    sender: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    subject: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    summary: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    deadline: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    processed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship(
        back_populates="emails"
    )

    reminders: Mapped[list["Reminder"]] = relationship(
        back_populates="email",
        cascade="all, delete-orphan"
    )