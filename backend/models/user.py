from __future__ import annotations # by this Email is not evaluated immediately but stored as string and sqlalchemy resolves it laeter
from datetime import datetime, timezone
from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base
from typing import TYPE_CHECKING
from sqlalchemy import String

#sqlalchemy builds metadata ie Base.metadata, alemibc sees the diff bet base.metadata and current db and does migration genertaion

if TYPE_CHECKING: # in case of circular imports it may crash so this helps. vs code still knows Email exists but actually dont import it at runtime
    from models.email import Email
    from models.telegram_token import TelegramConnectToken

class User(Base): # this tells sqlalchemy these are ORM models. w/o Base sqlAlchemy ignores the class
    __tablename__ = "users"

    id: Mapped[int] = mapped_column( # SQLAlchemy 2.0's typed ORM attribute tells SQLAlchemy and type checkers that this attribute is part of the ORM mapping and what Python type it holds.
        primary_key=True,     # mapped column creates actual col in db 
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

    emails: Mapped[list["Email"]] = relationship(  # Email is not defined here yet so __future__ annotation is there 
                                                    # it will not be evaluated instantly but postponed
                                                    # sqlalchemy resolves it later. it helps solve circular reference issues 
                        # relationship doesnt create a db column , but a python relationship 
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


# ForeignKey() -> this belongs to postgresql, it is enforced by db , like if user is deleted , email also deletes for him by db automatically thru foreignkey constarints
# cascade = "all, dlete-orphan" -> this belongs to sqlalchemy orm when working with py obj 

#timezone=True stores timezone-aware datetimes, typically in UTC. This avoids ambiguity and makes it easier to correctly display times for users in different time zones.
