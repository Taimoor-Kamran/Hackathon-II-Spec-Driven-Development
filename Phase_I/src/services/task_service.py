from typing import List, Optional
from datetime import datetime
from ..models.task import Task


class TaskService:
    """
    Handles all business operations for tasks:
    - Add task
    - Get all tasks
    - Get task by ID
    - Update task
    - Delete task
    - Mark task complete/incomplete
    - Validation logic
    """

    def __init__(self):
        """Initialize the task service with an empty in-memory storage."""
        self.tasks: List[Task] = []
        self.next_id = 1

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """Add a new task to the in-memory storage."""
        # Validate title
        if not (1 <= len(title) <= 200):
            raise ValueError("Title must be between 1 and 200 characters")

        # Create a new task
        task = Task(
            id=self.next_id,
            title=title,
            description=description
        )
        task.validate_title()

        # Add to storage
        self.tasks.append(task)
        self.next_id += 1

        return task

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks from storage."""
        return self.tasks

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Get a task by its ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: str = None, description: str = None) -> Optional[Task]:
        """Update an existing task."""
        task = self.get_task_by_id(task_id)
        if task is None:
            return None

        task.update(title, description)
        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID."""
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        self.tasks.remove(task)
        return True

    def mark_task_complete(self, task_id: int) -> Optional[Task]:
        """Mark a task as complete."""
        task = self.get_task_by_id(task_id)
        if task is None:
            return None

        task.completed = True
        task.updated_at = datetime.now()
        return task

    def mark_task_incomplete(self, task_id: int) -> Optional[Task]:
        """Mark a task as incomplete."""
        task = self.get_task_by_id(task_id)
        if task is None:
            return None

        task.completed = False
        task.updated_at = datetime.now()
        return task