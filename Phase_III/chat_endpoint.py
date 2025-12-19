"""
Stateless chat endpoint for Todo AI Chatbot
Persists conversation state to database
"""

from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, create_engine, Session, select, col
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
import json
import os

# Database Models
class ConversationState(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: str
    session_id: str
    messages: str  # JSON string of messages
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str


class ChatResponse(BaseModel):
    response: str
    session_id: str


# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///todo_phase_iii.db")
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Initialize database
create_db_and_tables()

# Import the AI agent after defining the models to avoid circular imports
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from todo_ai_agent import TodoAIChatbot

app = FastAPI(title="Todo AI Chatbot API", version="1.0.0")


def get_db():
    with Session(engine) as session:
        yield session


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Process a chat message and return AI response
    Persists conversation state to database
    """
    # Retrieve or create conversation state
    existing_state = db.exec(
        select(ConversationState)
        .where(ConversationState.user_id == request.user_id)
        .where(ConversationState.session_id == request.session_id)
    ).first()

    # Initialize the AI agent
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")

    chatbot = TodoAIChatbot(openai_api_key=openai_api_key)

    # Load conversation history if it exists
    if existing_state:
        try:
            messages = json.loads(existing_state.messages)
            chatbot.conversation_history = messages
        except json.JSONDecodeError:
            # If there's an error decoding the messages, start fresh
            chatbot.conversation_history = []

    # Process the user's message
    try:
        response = chatbot.process_user_input(request.message, request.user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

    # Save updated conversation state
    messages_json = json.dumps(chatbot.conversation_history)

    if existing_state:
        # Update existing state
        existing_state.messages = messages_json
        existing_state.updated_at = datetime.now()
        db.add(existing_state)
    else:
        # Create new state
        new_state = ConversationState(
            user_id=request.user_id,
            session_id=request.session_id,
            messages=messages_json
        )
        db.add(new_state)

    db.commit()

    return ChatResponse(response=response, session_id=request.session_id)


@app.get("/sessions/{user_id}")
def get_user_sessions(user_id: str, db: Session = Depends(get_db)):
    """
    Get all session IDs for a user
    """
    states = db.exec(
        select(ConversationState.session_id, ConversationState.updated_at)
        .where(ConversationState.user_id == user_id)
        .order_by(col(ConversationState.updated_at).desc())
    ).all()

    return [{"session_id": state.session_id, "last_updated": state.updated_at} for state in states]


@app.delete("/session/{session_id}")
def delete_session(session_id: str, user_id: str, db: Session = Depends(get_db)):
    """
    Delete a specific session
    """
    state = db.exec(
        select(ConversationState)
        .where(ConversationState.session_id == session_id)
        .where(ConversationState.user_id == user_id)
    ).first()

    if not state:
        raise HTTPException(status_code=404, detail="Session not found")

    db.delete(state)
    db.commit()

    return {"message": "Session deleted successfully"}


@app.get("/")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Todo AI Chatbot API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)