from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """
    Represents a single todo task with properties:
    - id: integer (auto-generated)
    - title: string (1-200 characters)
    - description: string (max 1000 characters, optional)
    - completed: boolean (default: false)
    - created_at: datetime
    - updated_at: datetime
    """
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        """Initialize timestamps if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = self.created_at

    def validate_title(self):
        """Validate the title length."""
        if not (1 <= len(self.title) <= 200):
            raise ValueError("Title must be between 1 and 200 characters")

    def update(self, title: str = None, description: str = None):
        """Update task details."""
        if title is not None:
            self.title = title
            self.validate_title()
        if description is not None:
            self.description = description
        self.updated_at = datetime.now()