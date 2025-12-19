from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from database import get_session
from models import Tag, TagCreate, TagUpdate, TagResponse
from services.tag_service import TagService
from auth import get_current_user

router = APIRouter()

@router.post("/tags", response_model=TagResponse)
def create_tag(
    tag: TagCreate,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new tag for the current user"""
    service = TagService(session)
    return service.create_tag(current_user.id, tag)


@router.get("/tags", response_model=List[TagResponse])
def get_tags(
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all tags for the current user"""
    service = TagService(session)
    return service.get_tags(current_user.id)


@router.get("/tags/{tag_id}", response_model=TagResponse)
def get_tag(
    tag_id: int,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific tag for the current user"""
    service = TagService(session)
    return service.get_tag(current_user.id, tag_id)


@router.put("/tags/{tag_id}", response_model=TagResponse)
def update_tag(
    tag_id: int,
    tag: TagUpdate,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a specific tag for the current user"""
    service = TagService(session)
    return service.update_tag(current_user.id, tag_id, tag)


@router.delete("/tags/{tag_id}")
def delete_tag(
    tag_id: int,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific tag for the current user"""
    service = TagService(session)
    success = service.delete_tag(current_user.id, tag_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found or doesn't belong to user"
        )
    return {"message": "Tag deleted successfully"}