"""
Simple Backend for Todo AI Chatbot
Handles API endpoints for the chatbot without MCP complexity
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import SQLModel, Field, create_engine, Session, select, delete
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime, timedelta
from uuid import UUID, uuid4
import os
import json
from dotenv import load_dotenv
from jose import JWTError, jwt

# Load environment variables
load_dotenv()

# Security configuration for JWT
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-jwt-key-change-this-in-production")
ALGORITHM = "HS256"

security = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_user_id_from_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Extract user ID from JWT token"""
    token = credentials.credentials
    payload = verify_token(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id


# Database Models
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    category_id: Optional[int] = None
    due_date: Optional[str] = None
    priority: str = "medium"
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    name: str
    color: str = "#000000"
    created_at: datetime = Field(default_factory=datetime.now)


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    name: str
    created_at: datetime = Field(default_factory=datetime.now)


class ConversationSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: str
    user_id: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class ConversationMessage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: str
    user_id: str
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)


# Pydantic models for API
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    due_date: Optional[str] = None
    priority: str = "medium"


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    category_id: Optional[int] = None
    due_date: Optional[str] = None
    priority: Optional[str] = None


class CategoryCreate(BaseModel):
    name: str
    color: str = "#000000"


class TagCreate(BaseModel):
    name: str


# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///todo_phase_iii.db")
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# FastAPI app
app = FastAPI(title="Todo AI Chatbot API", version="1.0.0")

# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def health_check():
    return {"status": "healthy", "service": "Todo AI Chatbot API"}


# Task endpoints
@app.get("/api/tasks")
def list_tasks_authenticated(user_id: str = Depends(get_user_id_from_token)):
    """List tasks for authenticated user using JWT token"""
    with Session(engine) as session:
        tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
        return tasks


@app.get("/api/{user_id}/tasks")
def list_tasks_legacy(user_id: str):
    """List tasks for user using legacy user_id parameter (for backward compatibility)"""
    with Session(engine) as session:
        tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
        return tasks


@app.post("/api/tasks")
def create_task_authenticated(task: TaskCreate, user_id: str = Depends(get_user_id_from_token)):
    """Create task for authenticated user using JWT token"""
    with Session(engine) as session:
        db_task = Task(
            user_id=user_id,
            title=task.title,
            description=task.description,
            category_id=task.category_id,
            due_date=task.due_date,
            priority=task.priority
        )
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task


@app.post("/api/{user_id}/tasks")
def create_task_legacy(user_id: str, task: TaskCreate):
    """Create task for user using legacy user_id parameter (for backward compatibility)"""
    with Session(engine) as session:
        db_task = Task(
            user_id=user_id,
            title=task.title,
            description=task.description,
            category_id=task.category_id,
            due_date=task.due_date,
            priority=task.priority
        )
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task


@app.put("/api/tasks/{task_id}")
def update_task_authenticated(task_id: int, task: TaskUpdate, user_id: str = Depends(get_user_id_from_token)):
    """Update task for authenticated user using JWT token"""
    with Session(engine) as session:
        db_task = session.get(Task, task_id)
        if not db_task or db_task.user_id != user_id:
            raise HTTPException(status_code=404, detail="Task not found")

        # Update only provided fields
        update_data = task.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)

        db_task.updated_at = datetime.now()
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task


@app.put("/api/{user_id}/tasks/{task_id}")
def update_task_legacy(user_id: str, task_id: int, task: TaskUpdate):
    """Update task for user using legacy user_id parameter (for backward compatibility)"""
    with Session(engine) as session:
        db_task = session.get(Task, task_id)
        if not db_task or db_task.user_id != user_id:
            raise HTTPException(status_code=404, detail="Task not found")

        # Update only provided fields
        update_data = task.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)

        db_task.updated_at = datetime.now()
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task


@app.delete("/api/tasks/{task_id}")
def delete_task_authenticated(task_id: int, user_id: str = Depends(get_user_id_from_token)):
    """Delete task for authenticated user using JWT token"""
    with Session(engine) as session:
        db_task = session.get(Task, task_id)
        if not db_task or db_task.user_id != user_id:
            raise HTTPException(status_code=404, detail="Task not found")

        session.delete(db_task)
        session.commit()
        return {"message": "Task deleted successfully"}


@app.delete("/api/{user_id}/tasks/{task_id}")
def delete_task_legacy(user_id: str, task_id: int):
    """Delete task for user using legacy user_id parameter (for backward compatibility)"""
    with Session(engine) as session:
        db_task = session.get(Task, task_id)
        if not db_task or db_task.user_id != user_id:
            raise HTTPException(status_code=404, detail="Task not found")

        session.delete(db_task)
        session.commit()
        return {"message": "Task deleted successfully"}


@app.delete("/api/tasks")
def delete_all_tasks_authenticated(user_id: str = Depends(get_user_id_from_token)):
    """Delete all tasks for authenticated user using JWT token"""
    with Session(engine) as session:
        # Delete all tasks for the user
        tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
        for task in tasks:
            session.delete(task)
        session.commit()
        return {"message": f"Deleted {len(tasks)} tasks successfully"}


@app.delete("/api/{user_id}/tasks")
def delete_all_tasks_legacy(user_id: str):
    """Delete all tasks for user using legacy user_id parameter (for backward compatibility)"""
    with Session(engine) as session:
        # Delete all tasks for the user
        tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
        for task in tasks:
            session.delete(task)
        session.commit()
        return {"message": f"Deleted {len(tasks)} tasks successfully"}


@app.delete("/api/categories")
def delete_all_categories_authenticated(user_id: str = Depends(get_user_id_from_token)):
    """Delete all categories for authenticated user using JWT token"""
    with Session(engine) as session:
        # Delete all categories for the user
        categories = session.exec(select(Category).where(Category.user_id == user_id)).all()
        for category in categories:
            session.delete(category)
        session.commit()
        return {"message": f"Deleted {len(categories)} categories successfully"}


@app.delete("/api/{user_id}/categories")
def delete_all_categories_legacy(user_id: str):
    """Delete all categories for user using legacy user_id parameter (for backward compatibility)"""
    with Session(engine) as session:
        # Delete all categories for the user
        categories = session.exec(select(Category).where(Category.user_id == user_id)).all()
        for category in categories:
            session.delete(category)
        session.commit()
        return {"message": f"Deleted {len(categories)} categories successfully"}


@app.delete("/api/tags")
def delete_all_tags_authenticated(user_id: str = Depends(get_user_id_from_token)):
    """Delete all tags for authenticated user using JWT token"""
    with Session(engine) as session:
        # Delete all tags for the user
        tags = session.exec(select(Tag).where(Tag.user_id == user_id)).all()
        for tag in tags:
            session.delete(tag)
        session.commit()
        return {"message": f"Deleted {len(tags)} tags successfully"}


@app.delete("/api/{user_id}/tags")
def delete_all_tags_legacy(user_id: str):
    """Delete all tags for user using legacy user_id parameter (for backward compatibility)"""
    with Session(engine) as session:
        # Delete all tags for the user
        tags = session.exec(select(Tag).where(Tag.user_id == user_id)).all()
        for tag in tags:
            session.delete(tag)
        session.commit()
        return {"message": f"Deleted {len(tags)} tags successfully"}


# Category endpoints
@app.get("/api/categories")
def list_categories_authenticated(user_id: str = Depends(get_user_id_from_token)):
    """List categories for authenticated user using JWT token"""
    with Session(engine) as session:
        categories = session.exec(select(Category).where(Category.user_id == user_id)).all()
        return categories


@app.get("/api/{user_id}/categories")
def list_categories_legacy(user_id: str):
    """List categories for user using legacy user_id parameter (for backward compatibility)"""
    with Session(engine) as session:
        categories = session.exec(select(Category).where(Category.user_id == user_id)).all()
        return categories


@app.post("/api/categories")
def create_category_authenticated(category: CategoryCreate, user_id: str = Depends(get_user_id_from_token)):
    """Create category for authenticated user using JWT token"""
    with Session(engine) as session:
        db_category = Category(
            user_id=user_id,
            name=category.name,
            color=category.color
        )
        session.add(db_category)
        session.commit()
        session.refresh(db_category)
        return db_category


@app.post("/api/{user_id}/categories")
def create_category_legacy(user_id: str, category: CategoryCreate):
    """Create category for user using legacy user_id parameter (for backward compatibility)"""
    with Session(engine) as session:
        db_category = Category(
            user_id=user_id,
            name=category.name,
            color=category.color
        )
        session.add(db_category)
        session.commit()
        session.refresh(db_category)
        return db_category


# Tag endpoints
@app.get("/api/tags")
def list_tags_authenticated(user_id: str = Depends(get_user_id_from_token)):
    """List tags for authenticated user using JWT token"""
    with Session(engine) as session:
        tags = session.exec(select(Tag).where(Tag.user_id == user_id)).all()
        return tags


@app.get("/api/{user_id}/tags")
def list_tags_legacy(user_id: str):
    """List tags for user using legacy user_id parameter (for backward compatibility)"""
    with Session(engine) as session:
        tags = session.exec(select(Tag).where(Tag.user_id == user_id)).all()
        return tags


@app.post("/api/tags")
def create_tag_authenticated(tag: TagCreate, user_id: str = Depends(get_user_id_from_token)):
    """Create tag for authenticated user using JWT token"""
    with Session(engine) as session:
        db_tag = Tag(
            user_id=user_id,
            name=tag.name
        )
        session.add(db_tag)
        session.commit()
        session.refresh(db_tag)
        return db_tag


@app.post("/api/{user_id}/tags")
def create_tag_legacy(user_id: str, tag: TagCreate):
    """Create tag for user using legacy user_id parameter (for backward compatibility)"""
    with Session(engine) as session:
        db_tag = Tag(
            user_id=user_id,
            name=tag.name
        )
        session.add(db_tag)
        session.commit()
        session.refresh(db_tag)
        return db_tag


from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str

# Legacy chat endpoint (the original one) - this is what the frontend uses
@app.post("/chat")
async def chat_endpoint_legacy(request: ChatRequest):
    """
    Legacy chat endpoint that accepts user_id in the request body (maintains backward compatibility with frontend)
    Uses AI agent to process natural language and interact with backend API
    """
    from todo_ai_agent import TodoAIChatbot
    import os

    # Store the message in the conversation history
    with Session(engine) as session:
        # Create or update session
        existing_session = session.exec(
            select(ConversationSession).where(ConversationSession.session_id == request.session_id)
        ).first()

        if not existing_session:
            new_session = ConversationSession(
                session_id=request.session_id,
                user_id=request.user_id
            )
            session.add(new_session)
            session.commit()

        # Store user message
        user_message = ConversationMessage(
            session_id=request.session_id,
            user_id=request.user_id,
            role="user",
            content=request.message
        )
        session.add(user_message)
        session.commit()

    # Process the message with the AI agent
    try:
        # Initialize the AI chatbot with the API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise Exception("OpenAI API key not found in environment")

        chatbot = TodoAIChatbot(openai_api_key=api_key, backend_url="http://localhost:8000")

        # Fetch conversation history from database to provide context
        # Only load user and assistant messages to avoid invalid message sequences
        with Session(engine) as session:
            # Get recent conversation messages for context (only user and assistant roles)
            history_messages = session.exec(
                select(ConversationMessage)
                .where(ConversationMessage.session_id == request.session_id)
                .where(ConversationMessage.user_id == request.user_id)
                .where(ConversationMessage.role.in_(["user", "assistant"]))  # Only user and assistant messages
                .order_by(ConversationMessage.timestamp)
                .limit(10)  # Only recent messages for context
            ).all()

            # Build context from history (only user and assistant messages)
            for msg in history_messages:
                if msg.role == "user":
                    chatbot.conversation_history.append({"role": "user", "content": msg.content})
                elif msg.role == "assistant":
                    chatbot.conversation_history.append({"role": "assistant", "content": msg.content})

        # Process the user input
        response = await chatbot.process_user_input(request.message, request.user_id)

        # Store the AI response in the conversation history
        with Session(engine) as session:
            ai_message = ConversationMessage(
                session_id=request.session_id,
                user_id=request.user_id,
                role="assistant",
                content=response
            )
            session.add(ai_message)
            session.commit()

        return {"response": response}
    except Exception as e:
        # In case of error with AI processing, return a helpful message
        error_response = f"I'm sorry, I encountered an error processing your request: {str(e)}. Please make sure your OpenAI API key is configured."

        # Store the error response in the conversation history
        with Session(engine) as session:
            ai_message = ConversationMessage(
                session_id=request.session_id,
                user_id=request.user_id,
                role="assistant",
                content=error_response
            )
            session.add(ai_message)
            session.commit()

        return {"response": error_response}


# New JWT-authenticated chat endpoint
class ChatRequestWithAuth(BaseModel):
    """Request model for JWT-authenticated chat endpoint"""
    session_id: str
    message: str


@app.post("/chat_authenticated")
async def chat_endpoint_authenticated(request: ChatRequestWithAuth, user_id: str = Depends(get_user_id_from_token)):
    """
    JWT-authenticated chat endpoint that extracts user_id from JWT token
    Uses AI agent to process natural language and interact with backend API
    """
    from todo_ai_agent import TodoAIChatbot
    import os

    # Store the message in the conversation history
    with Session(engine) as session:
        # Create or update session
        existing_session = session.exec(
            select(ConversationSession).where(ConversationSession.session_id == request.session_id)
        ).first()

        if not existing_session:
            new_session = ConversationSession(
                session_id=request.session_id,
                user_id=user_id  # From JWT token
            )
            session.add(new_session)
            session.commit()

        # Store user message
        user_message = ConversationMessage(
            session_id=request.session_id,
            user_id=user_id,  # From JWT token
            role="user",
            content=request.message
        )
        session.add(user_message)
        session.commit()

    # Process the message with the AI agent
    try:
        # Initialize the AI chatbot with the API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise Exception("OpenAI API key not found in environment")

        chatbot = TodoAIChatbot(openai_api_key=api_key, backend_url="http://localhost:8000")

        # Fetch conversation history from database to provide context
        # Only load user and assistant messages to avoid invalid message sequences
        with Session(engine) as session:
            # Get recent conversation messages for context (only user and assistant roles)
            history_messages = session.exec(
                select(ConversationMessage)
                .where(ConversationMessage.session_id == request.session_id)
                .where(ConversationMessage.user_id == user_id)  # From JWT token
                .where(ConversationMessage.role.in_(["user", "assistant"]))  # Only user and assistant messages
                .order_by(ConversationMessage.timestamp)
                .limit(10)  # Only recent messages for context
            ).all()

            # Build context from history (only user and assistant messages)
            for msg in history_messages:
                if msg.role == "user":
                    chatbot.conversation_history.append({"role": "user", "content": msg.content})
                elif msg.role == "assistant":
                    chatbot.conversation_history.append({"role": "assistant", "content": msg.content})

        # Process the user input
        response = await chatbot.process_user_input(request.message, user_id)

        # Store the AI response in the conversation history
        with Session(engine) as session:
            ai_message = ConversationMessage(
                session_id=request.session_id,
                user_id=user_id,  # From JWT token
                role="assistant",
                content=response
            )
            session.add(ai_message)
            session.commit()

        return {"response": response}
    except Exception as e:
        # In case of error with AI processing, return a helpful message
        error_response = f"I'm sorry, I encountered an error processing your request: {str(e)}. Please make sure your OpenAI API key is configured."

        # Store the error response in the conversation history
        with Session(engine) as session:
            ai_message = ConversationMessage(
                session_id=request.session_id,
                user_id=user_id,  # From JWT token
                role="assistant",
                content=error_response
            )
            session.add(ai_message)
            session.commit()

        return {"response": error_response}


# Authentication endpoints
@app.post("/auth/register")
def register_user(request: dict):
    """Register a new user and return JWT token"""
    # The frontend sends name, email, and password, but for this implementation
    # we'll use the email as the user identifier for simplicity
    email = request.get("email")
    name = request.get("name", "Default User")
    password = request.get("password")

    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

    # For this implementation, we'll use the email as the user_id
    # In a real system, we would create a user record in the database
    user_id = email

    # In a real system, we'd store user credentials securely
    # For this implementation, we'll just return a token with the user_id
    access_token = create_access_token(data={"sub": user_id})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/auth/login")
def login_user(request: dict):
    """Login a user and return JWT token"""
    # The frontend sends email and password
    email = request.get("email") or request.get("username")
    password = request.get("password")

    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

    # In a real system, we'd verify the password
    # For this implementation, we'll just return a token with the email as user_id
    access_token = create_access_token(data={"sub": email})
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)