from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import create_db_and_tables, get_session
from sqlmodel import Session
import models
from routes import auth, tasks, categories, tags, search, reminders, recurring, ai
from websocket import websocket_app

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    create_db_and_tables()
    yield

app = FastAPI(
    title="Phase III: Advanced Todo Web Application",
    description="Todo application with advanced features including AI-powered suggestions, real-time collaboration, advanced search, categories, tags, due dates, reminders, and recurring tasks",
    version="3.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(auth.router, prefix="/auth", tags=["authentication"])

# Include task routes
app.include_router(tasks.router, prefix="/api/{user_id}", tags=["tasks"])

# Include category routes
app.include_router(categories.router, prefix="/api/{user_id}", tags=["categories"])

# Include tag routes
app.include_router(tags.router, prefix="/api/{user_id}", tags=["tags"])

# Include search routes
app.include_router(search.router, prefix="/api/{user_id}", tags=["search"])

# Include reminder routes
app.include_router(reminders.router, prefix="/api/{user_id}", tags=["reminders"])

# Include recurring task routes
app.include_router(recurring.router, prefix="/api/{user_id}", tags=["recurring"])

# Include AI-powered suggestions routes
app.include_router(ai.router, prefix="/api/{user_id}", tags=["ai"])

# Include WebSocket routes
app.mount("/ws", websocket_app)

@app.get("/")
def read_root():
    return {"message": "Phase III Advanced Todo API", "version": "3.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Dependency to get database session
def get_db_session():
    with get_session() as session:
        yield session