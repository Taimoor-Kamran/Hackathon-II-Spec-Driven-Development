from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import List, Optional
from datetime import datetime
from database import get_session
from models import Task, TaskCreate, TaskUpdate, TaskResponse
from services.task_service import TaskService
from auth import get_current_user
from websocket import manager

router = APIRouter()

@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks(
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session),
    status: Optional[str] = Query(None, description="Filter by status (pending, completed)"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    tag_ids: Optional[List[int]] = Query(None, description="Filter by tag IDs"),
    due_date_start: Optional[datetime] = Query(None, description="Filter by due date start"),
    due_date_end: Optional[datetime] = Query(None, description="Filter by due date end"),
    priority: Optional[str] = Query(None, description="Filter by priority (low, medium, high)"),
    limit: int = Query(100, ge=1, le=1000, description="Number of results to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination")
):
    """Get all tasks for the current user with optional filters"""
    service = TaskService(session)
    return service.get_tasks(
        user_id=current_user.id,
        status_filter=status,
        category_id=category_id,
        tag_ids=tag_ids,
        due_date_start=due_date_start,
        due_date_end=due_date_end,
        priority=priority,
        limit=limit,
        offset=offset
    )


@router.post("/tasks", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    tag_ids: Optional[List[int]] = Query(None, description="Tag IDs to associate with the task"),
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new task for the current user"""
    service = TaskService(session)
    created_task = service.create_task(current_user.id, task, tag_ids=tag_ids)

    # Broadcast the new task to the user (for real-time updates)
    # In a real app with collaboration, you might broadcast to collaborators too
    message = {
        "type": "task_created",
        "task": created_task.dict(),
        "timestamp": datetime.now().isoformat()
    }
    manager.broadcast_to_user(str(message), current_user.id)

    return created_task


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific task for the current user"""
    service = TaskService(session)
    return service.get_task(current_user.id, task_id)


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task: TaskUpdate,
    tag_ids: Optional[List[int]] = Query(None, description="Tag IDs to associate with the task (pass empty list to remove all tags)"),
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a specific task for the current user"""
    service = TaskService(session)
    updated_task = service.update_task(current_user.id, task_id, task, tag_ids=tag_ids)

    # Broadcast the updated task to the user
    message = {
        "type": "task_updated",
        "task": updated_task.dict(),
        "timestamp": datetime.now().isoformat()
    }
    manager.broadcast_to_user(str(message), current_user.id)

    return updated_task


@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific task for the current user"""
    service = TaskService(session)
    success = service.delete_task(current_user.id, task_id)

    # Broadcast the deletion to the user
    message = {
        "type": "task_deleted",
        "task_id": task_id,
        "timestamp": datetime.now().isoformat()
    }
    manager.broadcast_to_user(str(message), current_user.id)

    if not success:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Task not found or doesn't belong to user")
    return {"message": "Task deleted successfully"}


@router.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
def toggle_task_completion(
    task_id: int,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Toggle the completion status of a task"""
    service = TaskService(session)
    toggled_task = service.toggle_task_completion(current_user.id, task_id)

    # Broadcast the completion status change to the user
    message = {
        "type": "task_completed",
        "task": toggled_task.dict(),
        "timestamp": datetime.now().isoformat()
    }
    manager.broadcast_to_user(str(message), current_user.id)

    return toggled_task


@router.post("/tasks/{task_id}/tags", response_model=TaskResponse)
def add_tags_to_task(
    task_id: int,
    tag_ids: List[int] = Query(..., description="List of tag IDs to add to the task"),
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Add tags to a specific task"""
    service = TaskService(session)
    updated_task = service.add_tags_to_task(current_user.id, task_id, tag_ids)

    # Broadcast the updated task to the user
    message = {
        "type": "task_updated",
        "task": updated_task.dict(),
        "timestamp": datetime.now().isoformat()
    }
    manager.broadcast_to_user(str(message), current_user.id)

    return updated_task


@router.delete("/tasks/{task_id}/tags", response_model=TaskResponse)
def remove_tags_from_task(
    task_id: int,
    tag_ids: List[int] = Query(..., description="List of tag IDs to remove from the task"),
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Remove tags from a specific task"""
    service = TaskService(session)
    updated_task = service.remove_tags_from_task(current_user.id, task_id, tag_ids)

    # Broadcast the updated task to the user
    message = {
        "type": "task_updated",
        "task": updated_task.dict(),
        "timestamp": datetime.now().isoformat()
    }
    manager.broadcast_to_user(str(message), current_user.id)

    return updated_task