from sqlmodel import Session, select
from typing import List
from models import Tag, TagCreate, TagUpdate, TagResponse, User, TaskTag
from fastapi import HTTPException, status

class TagService:
    def __init__(self, session: Session):
        self.session = session

    def create_tag(self, user_id: int, tag_data: TagCreate) -> TagResponse:
        """Create a new tag for a user"""
        # Verify user exists
        user = self.session.get(User, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Check if tag with same name already exists for this user
        existing_tag = self.session.exec(
            select(Tag)
            .where(Tag.user_id == user_id)
            .where(Tag.name == tag_data.name)
        ).first()

        if existing_tag:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tag with this name already exists"
            )

        # Create the tag
        tag = Tag(
            user_id=user_id,
            name=tag_data.name
        )

        self.session.add(tag)
        self.session.commit()
        self.session.refresh(tag)

        return self._tag_to_response(tag)

    def get_tags(self, user_id: int) -> List[TagResponse]:
        """Get all tags for a user"""
        tags = self.session.exec(
            select(Tag)
            .where(Tag.user_id == user_id)
        ).all()

        return [self._tag_to_response(tag) for tag in tags]

    def get_tag(self, user_id: int, tag_id: int) -> TagResponse:
        """Get a specific tag for a user"""
        tag = self.session.get(Tag, tag_id)
        if not tag or tag.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found or doesn't belong to user"
            )

        return self._tag_to_response(tag)

    def update_tag(self, user_id: int, tag_id: int, tag_data: TagUpdate) -> TagResponse:
        """Update a specific tag for a user"""
        tag = self.session.get(Tag, tag_id)
        if not tag or tag.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found or doesn't belong to user"
            )

        # Update name if provided
        if tag_data.name is not None:
            # Check if new name already exists for this user
            existing_tag = self.session.exec(
                select(Tag)
                .where(Tag.user_id == user_id)
                .where(Tag.name == tag_data.name)
                .where(Tag.id != tag_id)
            ).first()

            if existing_tag:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Tag with this name already exists"
                )

            tag.name = tag_data.name

        self.session.add(tag)
        self.session.commit()
        self.session.refresh(tag)

        return self._tag_to_response(tag)

    def delete_tag(self, user_id: int, tag_id: int) -> bool:
        """Delete a specific tag for a user"""
        tag = self.session.get(Tag, tag_id)
        if not tag or tag.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found or doesn't belong to user"
            )

        # Remove all task-tag associations first
        task_tags = self.session.exec(
            select(TaskTag)
            .where(TaskTag.tag_id == tag_id)
        ).all()

        for task_tag in task_tags:
            self.session.delete(task_tag)

        # Now delete the tag
        self.session.delete(tag)
        self.session.commit()
        return True

    def _tag_to_response(self, tag: Tag) -> TagResponse:
        """Convert Tag model to TagResponse"""
        return TagResponse(
            id=tag.id,
            user_id=tag.user_id,
            name=tag.name,
            created_at=tag.created_at,
            updated_at=tag.updated_at
        )