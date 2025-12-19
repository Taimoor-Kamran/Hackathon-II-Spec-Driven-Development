from sqlmodel import SQLModel, Field, create_engine, Session, Relationship
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, field_validator
from passlib.context import CryptContext
from enum import Enum


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class RecurrencePatternEnum(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    yearly = "yearly"


class UserBase(BaseModel):
    """Base model for user validation"""
    email: str
    name: Optional[str] = None

    @field_validator('email')
    def validate_email(cls, v):
        # Simple email validation
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v


class UserCreate(UserBase):
    """Model for creating a new user"""
    password: str

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        if len(v) > 72:
            raise ValueError('Password must be no more than 72 characters (bcrypt limitation)')
        return v


class UserUpdate(BaseModel):
    """Model for updating user"""
    name: Optional[str] = None
    email: Optional[str] = None


class UserResponse(UserBase):
    """Model for user response"""
    id: int
    created_at: datetime
    updated_at: datetime


class User(SQLModel, table=True):
    """SQLModel for users table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    name: Optional[str] = None
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    tasks: List["Task"] = Relationship(back_populates="user")
    categories: List["Category"] = Relationship(back_populates="user")
    tags: List["Tag"] = Relationship(back_populates="user")
    reminders: List["Reminder"] = Relationship(back_populates="user")

    def __setattr__(self, name, value):
        """Automatically update updated_at when any field is changed"""
        # Only update updated_at for actual field changes, not internal SQLAlchemy attributes
        if name != 'updated_at' and not name.startswith('_sa_'):
            super().__setattr__('updated_at', datetime.now())
        super().__setattr__(name, value)

    def verify_password(self, password: str) -> bool:
        """Verify a password against the hash"""
        return pwd_context.verify(password, self.password_hash)

    def set_password(self, password: str):
        """Hash and set the password"""
        self.password_hash = pwd_context.hash(password)


class TaskBase(BaseModel):
    """Base model for task validation"""
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False
    priority: Optional[PriorityEnum] = PriorityEnum.medium

    @field_validator('title')
    def validate_title_length(cls, v):
        if not (1 <= len(v) <= 200):
            raise ValueError('Title must be between 1 and 200 characters')
        return v

    @field_validator('description')
    def validate_description_length(cls, v):
        if v and len(v) > 1000:
            raise ValueError('Description must be less than 1000 characters')
        return v


class TaskCreate(TaskBase):
    """Model for creating a new task"""
    category_id: Optional[int] = None
    due_date: Optional[datetime] = None
    priority: Optional[PriorityEnum] = PriorityEnum.medium


class TaskUpdate(TaskBase):
    """Model for updating an existing task"""
    title: Optional[str] = None
    category_id: Optional[int] = None
    due_date: Optional[datetime] = None
    priority: Optional[PriorityEnum] = None


class TaskResponse(TaskBase):
    """Model for task response with all details"""
    id: int
    user_id: int
    completed: bool
    category_id: Optional[int] = None
    due_date: Optional[datetime] = None
    priority: PriorityEnum = PriorityEnum.medium
    created_at: datetime
    updated_at: datetime
    # Include related data
    category: Optional["CategoryResponse"] = None
    tags: List["TagResponse"] = []


class Task(SQLModel, table=True):
    """SQLModel for tasks table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")  # Foreign key to link to user
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    due_date: Optional[datetime] = None
    priority: PriorityEnum = Field(default=PriorityEnum.medium)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    user: User = Relationship(back_populates="tasks")
    category: Optional["Category"] = Relationship(back_populates="tasks")
    task_tags: List["TaskTag"] = Relationship(back_populates="task")
    reminders: List["Reminder"] = Relationship(back_populates="task")
    recurring_task: Optional["RecurringTask"] = Relationship(back_populates="original_task")

    def __setattr__(self, name, value):
        """Automatically update updated_at when any field is changed"""
        # Only update updated_at for actual field changes, not internal SQLAlchemy attributes
        if name != 'updated_at' and not name.startswith('_sa_'):
            super().__setattr__('updated_at', datetime.now())
        super().__setattr__(name, value)


class CategoryBase(BaseModel):
    """Base model for category validation"""
    name: str
    color: Optional[str] = "#000000"  # Default to black

    @field_validator('name')
    def validate_name_length(cls, v):
        if not (1 <= len(v) <= 50):
            raise ValueError('Category name must be between 1 and 50 characters')
        return v

    @field_validator('color')
    def validate_color_format(cls, v):
        if v and not v.startswith('#') and len(v) != 7:
            raise ValueError('Color must be in hex format (e.g., #FF0000)')
        return v


class CategoryCreate(CategoryBase):
    """Model for creating a new category"""
    pass


class CategoryUpdate(BaseModel):
    """Model for updating a category"""
    name: Optional[str] = None
    color: Optional[str] = None


class CategoryResponse(CategoryBase):
    """Model for category response"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class Category(SQLModel, table=True):
    """SQLModel for categories table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    name: str = Field(min_length=1, max_length=50)
    color: str = Field(default="#000000", max_length=7)  # Default to black
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    user: User = Relationship(back_populates="categories")
    tasks: List[Task] = Relationship(back_populates="category")

    def __setattr__(self, name, value):
        """Automatically update updated_at when any field is changed"""
        # Only update updated_at for actual field changes, not internal SQLAlchemy attributes
        if name != 'updated_at' and not name.startswith('_sa_'):
            super().__setattr__('updated_at', datetime.now())
        super().__setattr__(name, value)


class TagBase(BaseModel):
    """Base model for tag validation"""
    name: str

    @field_validator('name')
    def validate_name_length(cls, v):
        if not (1 <= len(v) <= 50):
            raise ValueError('Tag name must be between 1 and 50 characters')
        return v


class TagCreate(TagBase):
    """Model for creating a new tag"""
    pass


class TagUpdate(BaseModel):
    """Model for updating a tag"""
    name: Optional[str] = None


class TagResponse(TagBase):
    """Model for tag response"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class Tag(SQLModel, table=True):
    """SQLModel for tags table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    name: str = Field(min_length=1, max_length=50)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    user: User = Relationship(back_populates="tags")
    task_tags: List["TaskTag"] = Relationship(back_populates="tag")

    def __setattr__(self, name, value):
        """Automatically update updated_at when any field is changed"""
        # Only update updated_at for actual field changes, not internal SQLAlchemy attributes
        if name != 'updated_at' and not name.startswith('_sa_'):
            super().__setattr__('updated_at', datetime.now())
        super().__setattr__(name, value)


class TaskTagBase(BaseModel):
    """Base model for task-tag junction"""
    task_id: int
    tag_id: int


class TaskTagCreate(TaskTagBase):
    """Model for creating a task-tag association"""
    pass


class TaskTagResponse(TaskTagBase):
    """Model for task-tag response"""
    pass


class TaskTag(SQLModel, table=True):
    """SQLModel for task_tags junction table"""
    task_id: int = Field(foreign_key="task.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)

    # Relationships
    task: Task = Relationship(back_populates="task_tags")
    tag: Tag = Relationship(back_populates="task_tags")


class ReminderBase(BaseModel):
    """Base model for reminder validation"""
    task_id: int
    reminder_time: datetime
    sent: Optional[bool] = False


class ReminderCreate(ReminderBase):
    """Model for creating a new reminder"""
    pass


class ReminderUpdate(BaseModel):
    """Model for updating a reminder"""
    reminder_time: Optional[datetime] = None
    sent: Optional[bool] = None


class ReminderResponse(ReminderBase):
    """Model for reminder response"""
    id: int
    user_id: int
    created_at: datetime


class Reminder(SQLModel, table=True):
    """SQLModel for reminders table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id")
    user_id: int = Field(foreign_key="user.id")
    reminder_time: datetime
    sent: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    task: Task = Relationship(back_populates="reminders")
    user: User = Relationship(back_populates="reminders")


class RecurringTaskBase(BaseModel):
    """Base model for recurring task validation"""
    original_task_id: int
    recurrence_pattern: RecurrencePatternEnum
    interval: Optional[int] = 1
    end_date: Optional[datetime] = None


class RecurringTaskCreate(RecurringTaskBase):
    """Model for creating a recurring task pattern"""
    pass


class RecurringTaskUpdate(BaseModel):
    """Model for updating a recurring task pattern"""
    recurrence_pattern: Optional[RecurrencePatternEnum] = None
    interval: Optional[int] = None
    end_date: Optional[datetime] = None


class RecurringTaskResponse(RecurringTaskBase):
    """Model for recurring task response"""
    id: int
    created_at: datetime
    updated_at: datetime


class RecurringTask(SQLModel, table=True):
    """SQLModel for recurring_tasks table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    original_task_id: int = Field(foreign_key="task.id")
    recurrence_pattern: RecurrencePatternEnum
    interval: int = Field(default=1)
    end_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    original_task: Task = Relationship(back_populates="recurring_task")

    def __setattr__(self, name, value):
        """Automatically update updated_at when any field is changed"""
        # Only update updated_at for actual field changes, not internal SQLAlchemy attributes
        if name != 'updated_at' and not name.startswith('_sa_'):
            super().__setattr__('updated_at', datetime.now())
        super().__setattr__(name, value)