from sqlmodel import Session, select
from models import Task, TaskCreate, TaskUpdate, TaskResponse
from typing import List, Optional
from datetime import datetime


class TaskService:
    def __init__(self, session: Session):
        self.session = session

    def get_tasks_by_user_id(
        self,
        user_id: int,
        status_filter: Optional[str] = None,
        sort_by: Optional[str] = "created_at"
    ) -> List[TaskResponse]:
        """Get all tasks for a specific user with optional filtering and sorting"""
        query = select(Task).where(Task.user_id == user_id)

        # Apply status filter if provided
        if status_filter:
            if status_filter.lower() == "pending":
                query = query.where(Task.completed == False)
            elif status_filter.lower() == "completed":
                query = query.where(Task.completed == True)
            # If "all" or any other value, don't filter by status

        # Apply sorting
        if sort_by:
            if sort_by == "title":
                query = query.order_by(Task.title)
            elif sort_by == "created_at":
                query = query.order_by(Task.created_at.desc())
            # Add more sort options as needed

        tasks = self.session.exec(query).all()
        return [self._to_task_response(task) for task in tasks]

    def create_task(self, user_id: int, task_create: TaskCreate) -> TaskResponse:
        """Create a new task for a user"""
        # Validate the input data using the model
        task_create = TaskCreate(**task_create.model_dump())

        task = Task(
            user_id=user_id,
            title=task_create.title,
            description=task_create.description,
            completed=False  # Default to not completed
        )

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        return self._to_task_response(task)

    def get_task_by_id_and_user(self, task_id: int, user_id: int) -> Optional[TaskResponse]:
        """Get a specific task by ID for a specific user"""
        task = self.session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if task:
            return self._to_task_response(task)
        return None

    def update_task(self, task_id: int, user_id: int, task_update: TaskUpdate) -> Optional[TaskResponse]:
        """Update a specific task for a specific user"""
        task = self.session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if not task:
            return None

        # Update only provided fields
        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        task.updated_at = datetime.now()
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        return self._to_task_response(task)

    def delete_task(self, task_id: int, user_id: int) -> bool:
        """Delete a specific task for a specific user"""
        task = self.session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if not task:
            return False

        self.session.delete(task)
        self.session.commit()
        return True

    def toggle_task_completion(self, task_id: int, user_id: int) -> Optional[TaskResponse]:
        """Toggle the completion status of a specific task for a specific user"""
        task = self.session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if not task:
            return None

        task.completed = not task.completed
        task.updated_at = datetime.now()
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        return self._to_task_response(task)

    def _to_task_response(self, task: Task) -> TaskResponse:
        """Convert a Task model to a TaskResponse model"""
        return TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at,
            updated_at=task.updated_at
        )