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

    id: Mapped[int] = mapped_column( # here since it is primary key indexes are automatically generated. so index=true is reduntant here.
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column( # here it is the foreign key so it cant be null & ondelete cascade is tehre
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    gmail_message_id: Mapped[str] = mapped_column(# these are unqiue ids given by gmail to each mail
        String,
        unique=True,
        nullable=False
    )

    thread_id: Mapped[str] = mapped_column( # in future 1 mail can have many reminder so they are grouped by thread_id
        String,
        nullable=False
    )

    sender: Mapped[str] = mapped_column( # this is the sender's address 
        String,
        nullable=False
    )

    subject: Mapped[str] = mapped_column( # the subject of the mail
        String,
        nullable=False
    )

    summary: Mapped[str] = mapped_column( # the summary concluded by llm regarding th mail
        String,
        nullable=False
    )

    deadline: Mapped[datetime | None] = mapped_column( # this is the extracted deadline obtained by llm but can be null 
        DateTime(timezone=True),
        nullable=True
    )

    received_at: Mapped[datetime] = mapped_column( # this is the email receiving time 
        DateTime(timezone=True),
        nullable=False
    )

    processed_at: Mapped[datetime] = mapped_column( # this is the processed completion time so we can look out the latency
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship( # this is relationship not a column 
        back_populates="emails"
    )

    reminders: Mapped[list["Reminder"]] = relationship(
        back_populates="email",
        cascade="all, delete-orphan"
    )