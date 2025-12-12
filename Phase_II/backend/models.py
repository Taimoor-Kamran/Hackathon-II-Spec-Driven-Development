from sqlmodel import SQLModel, Field, create_engine, Session
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator
from passlib.context import CryptContext


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
    pass


class TaskUpdate(TaskBase):
    """Model for updating an existing task"""
    title: Optional[str] = None


class TaskResponse(TaskBase):
    """Model for task response with all details"""
    id: int
    user_id: int  # Changed from str to int to match user ID
    completed: bool
    created_at: datetime
    updated_at: datetime


class Task(SQLModel, table=True):
    """SQLModel for tasks table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int  # Changed from str to int to link to user ID
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def __setattr__(self, name, value):
        """Automatically update updated_at when any field is changed"""
        # Only update updated_at for actual field changes, not internal SQLAlchemy attributes
        if name != 'updated_at' and not name.startswith('_sa_'):
            super().__setattr__('updated_at', datetime.now())
        super().__setattr__(name, value)