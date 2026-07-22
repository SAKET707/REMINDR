from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import get_current_user, get_db
from models.user import User
from schemas.preparation_task_schema import (
    PreparationTaskCreateRequest,
    PreparationTaskResponse,
    PreparationTaskUpdateRequest,
)
from services.preparation_task_service import PreparationTaskService

router = APIRouter(
    prefix="/preparation-tasks",
    tags=["Preparation Tasks"],
)

@router.get(
    "/reminder/{reminder_id}",
    response_model=list[PreparationTaskResponse],
)
def get_preparation_tasks(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return PreparationTaskService.get_all(
        db=db,
        reminder_id=reminder_id,
        user_id=current_user.id,
    )

@router.get(
    "/",
    response_model=list[PreparationTaskResponse],
)
def get_all_preparation_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return PreparationTaskService.get_all_for_user(
        db=db,
        user_id=current_user.id,
    )

@router.post(
    "/reminder/{reminder_id}",
    response_model=PreparationTaskResponse,
)
def create_preparation_task(
    reminder_id: int,
    request: PreparationTaskCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return PreparationTaskService.create(
        db=db,
        reminder_id=reminder_id,
        user_id=current_user.id,
        title=request.title,
    )

@router.patch(
    "/{task_id}",
    response_model=PreparationTaskResponse,
)
def update_preparation_task(
    task_id: int,
    request: PreparationTaskUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return PreparationTaskService.update(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
        title=request.title,
        completed=request.completed,
    )

@router.delete("/{task_id}")
def delete_preparation_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    PreparationTaskService.delete(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
    )

    return {
        "message": "Preparation task deleted successfully."
    }