from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from database import get_session
from models import TaskResponse
from services.ai_service import AIService
from auth import get_current_user

router = APIRouter()

@router.get("/tasks/suggest", response_model=List[TaskResponse])
def get_task_suggestions(
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session),
    limit: int = 5
):
    """Get AI-powered task suggestions for the current user"""
    service = AIService(session)
    return service.get_task_suggestions(current_user.id, limit)


@router.get("/analysis")
def analyze_user_patterns(
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Analyze user's task patterns and provide insights"""
    service = AIService(session)
    return service.analyze_user_patterns(current_user.id)