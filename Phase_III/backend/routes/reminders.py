from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from database import get_session
from models import Reminder, ReminderCreate, ReminderUpdate, ReminderResponse
from services.reminder_service import ReminderService
from auth import get_current_user

router = APIRouter()

@router.post("/reminders", response_model=ReminderResponse)
def create_reminder(
    reminder: ReminderCreate,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new reminder for the current user"""
    service = ReminderService(session)
    return service.create_reminder(current_user.id, reminder)


@router.get("/reminders", response_model=List[ReminderResponse])
def get_reminders(
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all reminders for the current user"""
    service = ReminderService(session)
    return service.get_reminders(current_user.id)


@router.get("/reminders/{reminder_id}", response_model=ReminderResponse)
def get_reminder(
    reminder_id: int,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific reminder for the current user"""
    service = ReminderService(session)
    return service.get_reminder(current_user.id, reminder_id)


@router.put("/reminders/{reminder_id}", response_model=ReminderResponse)
def update_reminder(
    reminder_id: int,
    reminder: ReminderUpdate,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a specific reminder for the current user"""
    service = ReminderService(session)
    return service.update_reminder(current_user.id, reminder_id, reminder)


@router.delete("/reminders/{reminder_id}")
def delete_reminder(
    reminder_id: int,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific reminder for the current user"""
    service = ReminderService(session)
    success = service.delete_reminder(current_user.id, reminder_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found or doesn't belong to user"
        )
    return {"message": "Reminder deleted successfully"}


@router.get("/reminders/upcoming", response_model=List[ReminderResponse])
def get_upcoming_reminders(
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session),
    limit: int = 10
):
    """Get upcoming reminders that haven't been sent yet"""
    service = ReminderService(session)
    return service.get_upcoming_reminders(current_user.id, limit)


@router.post("/reminders/{reminder_id}/mark-sent")
def mark_reminder_as_sent(
    reminder_id: int,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Mark a specific reminder as sent"""
    service = ReminderService(session)
    success = service.mark_reminder_as_sent(reminder_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found"
        )
    return {"message": "Reminder marked as sent successfully"}