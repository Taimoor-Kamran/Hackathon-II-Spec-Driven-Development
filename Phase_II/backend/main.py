from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import tasks
from routes.auth import router as auth_router
import os
from dotenv import load_dotenv
from database import create_db_and_tables

# Load environment variables
load_dotenv()

# Create FastAPI app instance
app = FastAPI(
    title="Todo API - Phase II",
    description="Full-Stack Todo Application API with authentication",
    version="1.0.0"
)

# Create database tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(tasks.router, prefix="/api/{user_id}", tags=["tasks"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Todo API - Phase II is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}