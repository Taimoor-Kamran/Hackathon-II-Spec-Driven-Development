from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from database import get_session
from models import Category, CategoryCreate, CategoryUpdate, CategoryResponse
from services.category_service import CategoryService
from auth import get_current_user

router = APIRouter()

@router.post("/categories", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new category for the current user"""
    service = CategoryService(session)
    return service.create_category(current_user.id, category)


@router.get("/categories", response_model=List[CategoryResponse])
def get_categories(
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all categories for the current user"""
    service = CategoryService(session)
    return service.get_categories(current_user.id)


@router.get("/categories/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific category for the current user"""
    service = CategoryService(session)
    return service.get_category(current_user.id, category_id)


@router.put("/categories/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a specific category for the current user"""
    service = CategoryService(session)
    return service.update_category(current_user.id, category_id, category)


@router.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific category for the current user"""
    service = CategoryService(session)
    success = service.delete_category(current_user.id, category_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found or doesn't belong to user"
        )
    return {"message": "Category deleted successfully"}