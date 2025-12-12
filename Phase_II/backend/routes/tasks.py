from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime
from models import Task, TaskCreate, TaskUpdate, TaskResponse
from database import get_session, create_db_and_tables
from auth import get_current_user, verify_user_id_match, TokenData
from services.task_service import TaskService

# Create router
router = APIRouter()

@router.get("/tasks", response_model=List[TaskResponse])
def list_tasks(
    user_id: str,
    current_user: TokenData = Depends(get_current_user),
    status_filter: Optional[str] = Query(None, description="Filter by status: 'pending', 'completed', or 'all'"),
    sort_by: Optional[str] = Query("created_at", description="Sort by: 'created_at', 'title', 'due_date'"),
    session: Session = Depends(get_session)
):
    """List all tasks for the specified user"""
    # Verify that the user_id in the token matches the user_id in the URL
    if not verify_user_id_match(current_user.user_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's tasks"
        )

    # Use the TaskService to get tasks
    task_service = TaskService(session)
    tasks = task_service.get_tasks_by_user_id(
        user_id=user_id,
        status_filter=status_filter,
        sort_by=sort_by
    )

    return tasks


@router.post("/tasks", response_model=TaskResponse)
def create_task(
    user_id: str,
    task_create: TaskCreate,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new task for the specified user"""
    # Verify that the user_id in the token matches the user_id in the URL
    if not verify_user_id_match(current_user.user_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )

    # Use the TaskService to create the task
    task_service = TaskService(session)
    task = task_service.create_task(user_id=user_id, task_create=task_create)

    return task


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    user_id: str,
    task_id: int,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific task by ID for the specified user"""
    # Verify that the user_id in the token matches the user_id in the URL
    if not verify_user_id_match(current_user.user_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's tasks"
        )

    # Use the TaskService to get the task
    task_service = TaskService(session)
    task = task_service.get_task_by_id_and_user(task_id=task_id, user_id=user_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    user_id: str,
    task_id: int,
    task_update: TaskUpdate,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a specific task by ID for the specified user"""
    # Verify that the user_id in the token matches the user_id in the URL
    if not verify_user_id_match(current_user.user_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user's tasks"
        )

    # Use the TaskService to update the task
    task_service = TaskService(session)
    updated_task = task_service.update_task(
        task_id=task_id,
        user_id=user_id,
        task_update=task_update
    )

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return updated_task


@router.delete("/tasks/{task_id}")
def delete_task(
    user_id: str,
    task_id: int,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific task by ID for the specified user"""
    # Verify that the user_id in the token matches the user_id in the URL
    if not verify_user_id_match(current_user.user_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user's tasks"
        )

    # Use the TaskService to delete the task
    task_service = TaskService(session)
    success = task_service.delete_task(task_id=task_id, user_id=user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return {"message": "Task deleted successfully"}


@router.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
def toggle_task_completion(
    user_id: str,
    task_id: int,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Toggle the completion status of a specific task by ID for the specified user"""
    # Verify that the user_id in the token matches the user_id in the URL
    if not verify_user_id_match(current_user.user_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user's tasks"
        )

    # Use the TaskService to toggle task completion
    task_service = TaskService(session)
    updated_task = task_service.toggle_task_completion(task_id=task_id, user_id=user_id)

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return updated_task