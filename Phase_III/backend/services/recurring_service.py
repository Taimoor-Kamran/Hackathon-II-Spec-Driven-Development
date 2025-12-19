from sqlmodel import Session, select
from typing import List
from datetime import datetime, timedelta
from models import RecurringTask, RecurringTaskCreate, RecurringTaskUpdate, RecurringTaskResponse, Task, TaskTag
from fastapi import HTTPException, status

class RecurringTaskService:
    def __init__(self, session: Session):
        self.session = session

    def create_recurring_task(self, recurring_data: RecurringTaskCreate) -> RecurringTaskResponse:
        """Create a new recurring task pattern"""
        # Verify the original task exists
        original_task = self.session.get(Task, recurring_data.original_task_id)
        if not original_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Original task not found"
            )

        # Create the recurring task pattern
        recurring_task = RecurringTask(
            original_task_id=recurring_data.original_task_id,
            recurrence_pattern=recurring_data.recurrence_pattern,
            interval=recurring_data.interval or 1,
            end_date=recurring_data.end_date
        )

        self.session.add(recurring_task)
        self.session.commit()
        self.session.refresh(recurring_task)

        return self._recurring_task_to_response(recurring_task)

    def get_recurring_tasks(self, user_id: int) -> List[RecurringTaskResponse]:
        """Get all recurring task patterns for a user"""
        recurring_tasks = self.session.exec(
            select(RecurringTask)
            .join(Task)
            .where(Task.user_id == user_id)
        ).all()

        return [self._recurring_task_to_response(recurring_task) for recurring_task in recurring_tasks]

    def get_recurring_task(self, user_id: int, recurring_task_id: int) -> RecurringTaskResponse:
        """Get a specific recurring task pattern for a user"""
        recurring_task = self.session.get(RecurringTask, recurring_task_id)
        if not recurring_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recurring task not found"
            )

        # Verify that the original task belongs to the user
        original_task = self.session.get(Task, recurring_task.original_task_id)
        if not original_task or original_task.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recurring task not found or doesn't belong to user"
            )

        return self._recurring_task_to_response(recurring_task)

    def update_recurring_task(self, user_id: int, recurring_task_id: int, recurring_data: RecurringTaskUpdate) -> RecurringTaskResponse:
        """Update a specific recurring task pattern for a user"""
        recurring_task = self.session.get(RecurringTask, recurring_task_id)
        if not recurring_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recurring task not found"
            )

        # Verify that the original task belongs to the user
        original_task = self.session.get(Task, recurring_task.original_task_id)
        if not original_task or original_task.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recurring task not found or doesn't belong to user"
            )

        # Update fields if provided
        if recurring_data.recurrence_pattern is not None:
            recurring_task.recurrence_pattern = recurring_data.recurrence_pattern
        if recurring_data.interval is not None:
            recurring_task.interval = recurring_data.interval
        if recurring_data.end_date is not None:
            recurring_task.end_date = recurring_data.end_date

        self.session.add(recurring_task)
        self.session.commit()
        self.session.refresh(recurring_task)

        return self._recurring_task_to_response(recurring_task)

    def delete_recurring_task(self, user_id: int, recurring_task_id: int) -> bool:
        """Delete a specific recurring task pattern for a user"""
        recurring_task = self.session.get(RecurringTask, recurring_task_id)
        if not recurring_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recurring task not found"
            )

        # Verify that the original task belongs to the user
        original_task = self.session.get(Task, recurring_task.original_task_id)
        if not original_task or original_task.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recurring task not found or doesn't belong to user"
            )

        self.session.delete(recurring_task)
        self.session.commit()
        return True

    def generate_future_instances(self, recurring_task_id: int, count: int = 10) -> List[Task]:
        """Generate future task instances based on the recurring pattern"""
        recurring_task = self.session.get(RecurringTask, recurring_task_id)
        if not recurring_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recurring task not found"
            )

        original_task = self.session.get(Task, recurring_task.original_task_id)
        if not original_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Original task not found"
            )

        # Get the tag associations of the original task to copy to new instances
        original_task_tags = self.session.exec(
            select(TaskTag).where(TaskTag.task_id == original_task.id)
        ).all()

        # Get the last generated instance to know where to start from
        # For simplicity, we'll just generate from now
        current_date = datetime.now()
        future_instances = []

        for i in range(count):
            new_task_date = self._calculate_next_date(
                current_date,
                recurring_task.recurrence_pattern,
                recurring_task.interval
            )

            # Check if we've reached the end date
            if recurring_task.end_date and new_task_date > recurring_task.end_date:
                break

            # Create a new task instance based on the original
            new_task = Task(
                user_id=original_task.user_id,
                title=original_task.title,
                description=original_task.description,
                completed=False,  # New instances are not completed
                category_id=original_task.category_id,
                due_date=new_task_date,  # Set the due date based on recurrence
                priority=original_task.priority
            )

            self.session.add(new_task)
            self.session.commit()
            self.session.refresh(new_task)

            # Copy tag associations to the new task
            for task_tag in original_task_tags:
                new_task_tag = TaskTag(
                    task_id=new_task.id,
                    tag_id=task_tag.tag_id
                )
                self.session.add(new_task_tag)

            self.session.commit()
            self.session.refresh(new_task)

            future_instances.append(new_task)
            current_date = new_task_date

        return future_instances

    def _calculate_next_date(self, start_date: datetime, pattern: str, interval: int) -> datetime:
        """Calculate the next date based on recurrence pattern"""
        if pattern == "daily":
            return start_date + timedelta(days=interval)
        elif pattern == "weekly":
            return start_date + timedelta(weeks=interval)
        elif pattern == "monthly":
            # Add months by calculating the target month and year
            month = start_date.month - 1 + interval
            year = start_date.year + month // 12
            month = month % 12 + 1
            day = min(start_date.day, [31,
                29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
                31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month-1])
            return start_date.replace(year=year, month=month, day=day)
        elif pattern == "yearly":
            return start_date.replace(year=start_date.year + interval)
        else:
            # Default to daily if pattern is unknown
            return start_date + timedelta(days=interval)

    def _recurring_task_to_response(self, recurring_task: RecurringTask) -> RecurringTaskResponse:
        """Convert RecurringTask model to RecurringTaskResponse"""
        return RecurringTaskResponse(
            id=recurring_task.id,
            original_task_id=recurring_task.original_task_id,
            recurrence_pattern=recurring_task.recurrence_pattern,
            interval=recurring_task.interval,
            end_date=recurring_task.end_date,
            created_at=recurring_task.created_at,
            updated_at=recurring_task.updated_at
        )