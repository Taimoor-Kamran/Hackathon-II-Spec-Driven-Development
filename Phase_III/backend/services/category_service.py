from sqlmodel import Session, select
from typing import List
from models import Category, CategoryCreate, CategoryUpdate, CategoryResponse, User, Task
from fastapi import HTTPException, status

class CategoryService:
    def __init__(self, session: Session):
        self.session = session

    def create_category(self, user_id: int, category_data: CategoryCreate) -> CategoryResponse:
        """Create a new category for a user"""
        # Verify user exists
        user = self.session.get(User, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Check if category with same name already exists for this user
        existing_category = self.session.exec(
            select(Category)
            .where(Category.user_id == user_id)
            .where(Category.name == category_data.name)
        ).first()

        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this name already exists"
            )

        # Create the category
        category = Category(
            user_id=user_id,
            name=category_data.name,
            color=category_data.color
        )

        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)

        return self._category_to_response(category)

    def get_categories(self, user_id: int) -> List[CategoryResponse]:
        """Get all categories for a user"""
        categories = self.session.exec(
            select(Category)
            .where(Category.user_id == user_id)
        ).all()

        return [self._category_to_response(category) for category in categories]

    def get_category(self, user_id: int, category_id: int) -> CategoryResponse:
        """Get a specific category for a user"""
        category = self.session.get(Category, category_id)
        if not category or category.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found or doesn't belong to user"
            )

        return self._category_to_response(category)

    def update_category(self, user_id: int, category_id: int, category_data: CategoryUpdate) -> CategoryResponse:
        """Update a specific category for a user"""
        category = self.session.get(Category, category_id)
        if not category or category.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found or doesn't belong to user"
            )

        # Update fields if provided
        if category_data.name is not None:
            category.name = category_data.name
        if category_data.color is not None:
            category.color = category_data.color

        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)

        return self._category_to_response(category)

    def delete_category(self, user_id: int, category_id: int) -> bool:
        """Delete a specific category for a user"""
        category = self.session.get(Category, category_id)
        if not category or category.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found or doesn't belong to user"
            )

        # Update all tasks that use this category to have no category
        # This handles the foreign key constraint properly
        tasks_with_category = self.session.exec(
            select(Task).where(Task.category_id == category_id)
        ).all()

        for task in tasks_with_category:
            task.category_id = None

        # Now delete the category
        self.session.delete(category)
        self.session.commit()
        return True

    def _category_to_response(self, category: Category) -> CategoryResponse:
        """Convert Category model to CategoryResponse"""
        return CategoryResponse(
            id=category.id,
            user_id=category.user_id,
            name=category.name,
            color=category.color,
            created_at=category.created_at,
            updated_at=category.updated_at
        )