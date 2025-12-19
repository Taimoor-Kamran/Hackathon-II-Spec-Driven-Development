from sqlmodel import create_engine, Session
from models import SQLModel
from typing import Generator
import os

# Get database URL from environment variable, default to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app_phase3.db")

# Create engine with appropriate settings for SQLite
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True to see SQL queries in logs
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    pool_pre_ping=True,  # Verify connections before use
)

def create_db_and_tables():
    """Create database tables based on models"""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Get database session for dependency injection"""
    with Session(engine) as session:
        yield session