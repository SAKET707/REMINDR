from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PreparationTaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    completed: bool
    position: int
    created_at: datetime
    updated_at: datetime
    reminder_id: int


class PreparationTaskCreateRequest(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255,
    )

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Title cannot be empty.")

        return value


class PreparationTaskUpdateRequest(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    completed: bool | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str | None) -> str | None:
        if value is None:
            return value

        value = value.strip()

        if not value:
            raise ValueError("Title cannot be empty.")

        return value