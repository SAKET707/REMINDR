from __future__ import annotations
from datetime import datetime, timezone
from models.preparation_task import PreparationTask
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

if TYPE_CHECKING:
    from models.email import Email
    from models.preparation_task import PreparationTask


class Reminder(Base):
    __tablename__ = "reminders"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    email_id: Mapped[int] = mapped_column(
        ForeignKey("emails.id", ondelete="CASCADE"),
        nullable=False
    )

    scheduled_for: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String,
        default="PENDING",
        nullable=False
    )

    sent_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    email: Mapped["Email"] = relationship(
        back_populates="reminders"
    )

    preparation_tasks: Mapped[list["PreparationTask"]] = relationship(
        back_populates="reminder",
        cascade="all, delete-orphan",
    )