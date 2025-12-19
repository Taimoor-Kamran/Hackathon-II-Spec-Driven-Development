from sqlmodel import Session, select
from typing import List
from datetime import datetime
from models import Reminder, ReminderCreate, ReminderUpdate, ReminderResponse, User, Task
from fastapi import HTTPException, status

class ReminderService:
    def __init__(self, session: Session):
        self.session = session

    def create_reminder(self, user_id: int, reminder_data: ReminderCreate) -> ReminderResponse:
        """Create a new reminder for a user"""
        # Verify user exists
        user = self.session.get(User, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Verify task exists and belongs to user
        task = self.session.get(Task, reminder_data.task_id)
        if not task or task.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or doesn't belong to user"
            )

        # Create the reminder
        reminder = Reminder(
            task_id=reminder_data.task_id,
            user_id=user_id,
            reminder_time=reminder_data.reminder_time,
            sent=reminder_data.sent or False
        )

        self.session.add(reminder)
        self.session.commit()
        self.session.refresh(reminder)

        return self._reminder_to_response(reminder)

    def get_reminders(self, user_id: int) -> List[ReminderResponse]:
        """Get all reminders for a user"""
        reminders = self.session.exec(
            select(Reminder)
            .where(Reminder.user_id == user_id)
        ).all()

        return [self._reminder_to_response(reminder) for reminder in reminders]

    def get_reminder(self, user_id: int, reminder_id: int) -> ReminderResponse:
        """Get a specific reminder for a user"""
        reminder = self.session.get(Reminder, reminder_id)
        if not reminder or reminder.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reminder not found or doesn't belong to user"
            )

        return self._reminder_to_response(reminder)

    def update_reminder(self, user_id: int, reminder_id: int, reminder_data: ReminderUpdate) -> ReminderResponse:
        """Update a specific reminder for a user"""
        reminder = self.session.get(Reminder, reminder_id)
        if not reminder or reminder.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reminder not found or doesn't belong to user"
            )

        # Update fields if provided
        if reminder_data.reminder_time is not None:
            reminder.reminder_time = reminder_data.reminder_time
        if reminder_data.sent is not None:
            reminder.sent = reminder_data.sent

        self.session.add(reminder)
        self.session.commit()
        self.session.refresh(reminder)

        return self._reminder_to_response(reminder)

    def delete_reminder(self, user_id: int, reminder_id: int) -> bool:
        """Delete a specific reminder for a user"""
        reminder = self.session.get(Reminder, reminder_id)
        if not reminder or reminder.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reminder not found or doesn't belong to user"
            )

        self.session.delete(reminder)
        self.session.commit()
        return True

    def get_upcoming_reminders(self, user_id: int, limit: int = 10) -> List[ReminderResponse]:
        """Get upcoming reminders that haven't been sent yet"""
        reminders = self.session.exec(
            select(Reminder)
            .where(Reminder.user_id == user_id)
            .where(Reminder.sent == False)
            .where(Reminder.reminder_time >= datetime.now())
            .order_by(Reminder.reminder_time.asc())
            .limit(limit)
        ).all()

        return [self._reminder_to_response(reminder) for reminder in reminders]

    def mark_reminder_as_sent(self, reminder_id: int) -> bool:
        """Mark a reminder as sent"""
        reminder = self.session.get(Reminder, reminder_id)
        if not reminder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reminder not found"
            )

        reminder.sent = True
        self.session.add(reminder)
        self.session.commit()
        return True

    def _reminder_to_response(self, reminder: Reminder) -> ReminderResponse:
        """Convert Reminder model to ReminderResponse"""
        return ReminderResponse(
            id=reminder.id,
            task_id=reminder.task_id,
            user_id=reminder.user_id,
            reminder_time=reminder.reminder_time,
            sent=reminder.sent,
            created_at=reminder.created_at
        )