from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from database import get_session
from models import RecurringTask, RecurringTaskCreate, RecurringTaskUpdate, RecurringTaskResponse
from services.recurring_service import RecurringTaskService
from auth import get_current_user

router = APIRouter()

@router.post("/recurring", response_model=RecurringTaskResponse)
def create_recurring_task(
    recurring_task: RecurringTaskCreate,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new recurring task pattern for the current user"""
    service = RecurringTaskService(session)
    return service.create_recurring_task(recurring_task)


@router.get("/recurring", response_model=List[RecurringTaskResponse])
def get_recurring_tasks(
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all recurring task patterns for the current user"""
    service = RecurringTaskService(session)
    return service.get_recurring_tasks(current_user.id)


@router.get("/recurring/{recurring_task_id}", response_model=RecurringTaskResponse)
def get_recurring_task(
    recurring_task_id: int,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific recurring task pattern for the current user"""
    service = RecurringTaskService(session)
    return service.get_recurring_task(current_user.id, recurring_task_id)


@router.put("/recurring/{recurring_task_id}", response_model=RecurringTaskResponse)
def update_recurring_task(
    recurring_task_id: int,
    recurring_task: RecurringTaskUpdate,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a specific recurring task pattern for the current user"""
    service = RecurringTaskService(session)
    return service.update_recurring_task(current_user.id, recurring_task_id, recurring_task)


@router.delete("/recurring/{recurring_task_id}")
def delete_recurring_task(
    recurring_task_id: int,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific recurring task pattern for the current user"""
    service = RecurringTaskService(session)
    success = service.delete_recurring_task(current_user.id, recurring_task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurring task not found or doesn't belong to user"
        )
    return {"message": "Recurring task deleted successfully"}


@router.post("/recurring/{recurring_task_id}/generate-instances")
def generate_recurring_instances(
    recurring_task_id: int,
    count: int = 10,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Generate future task instances based on a recurring pattern"""
    service = RecurringTaskService(session)
    instances = service.generate_future_instances(recurring_task_id, count)
    return {"message": f"Generated {len(instances)} task instances", "instances": [instance.id for instance in instances]}