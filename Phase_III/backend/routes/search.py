from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import List, Optional
from datetime import datetime
from database import get_session
from models import TaskResponse
from services.task_service import TaskService
from auth import get_current_user

router = APIRouter()

@router.get("/tasks/search", response_model=List[TaskResponse])
def search_tasks(
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session),
    query: Optional[str] = Query(None, description="Search query for title or description"),
    status: Optional[str] = Query(None, description="Filter by status (pending, completed)"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    tag_ids: Optional[List[int]] = Query(None, description="Filter by tag IDs"),
    due_date_start: Optional[datetime] = Query(None, description="Filter by due date start"),
    due_date_end: Optional[datetime] = Query(None, description="Filter by due date end"),
    priority: Optional[str] = Query(None, description="Filter by priority (low, medium, high)"),
    sort_by: Optional[str] = Query(None, description="Sort by field (title, due_date, priority, created_at)"),
    sort_order: Optional[str] = Query("asc", description="Sort order (asc, desc)"),
    limit: int = Query(20, ge=1, le=100, description="Number of results to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination")
):
    """Search and filter tasks with advanced options"""
    service = TaskService(session)
    return service.search_tasks(
        user_id=current_user.id,
        search_query=query,
        status_filter=status,
        category_id=category_id,
        tag_ids=tag_ids,
        due_date_start=due_date_start,
        due_date_end=due_date_end,
        priority=priority,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit,
        offset=offset
    )


@router.get("/tasks/suggestions", response_model=List[TaskResponse])
def get_task_suggestions(
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session),
    limit: int = Query(5, ge=1, le=20, description="Number of suggestions to return")
):
    """Get AI-powered task suggestions for the current user"""
    from services.ai_service import AIService
    service = AIService(session)
    return service.get_task_suggestions(current_user.id, limit)