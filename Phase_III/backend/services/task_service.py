from sqlmodel import Session, select, and_
from typing import List, Optional
from datetime import datetime
from models import Task, TaskCreate, TaskUpdate, User, Category, Tag, TaskTag, TaskResponse
from fastapi import HTTPException, status

class TaskService:
    def __init__(self, session: Session):
        self.session = session

    def create_task(self, user_id: int, task_data: TaskCreate, tag_ids: Optional[List[int]] = None) -> TaskResponse:
        """Create a new task for a user"""
        # Verify user exists
        user = self.session.get(User, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Verify category exists and belongs to user (if provided)
        if task_data.category_id:
            category = self.session.get(Category, task_data.category_id)
            if not category or category.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Category not found or doesn't belong to user"
                )

        # Verify tag IDs belong to user (if provided)
        if tag_ids:
            for tag_id in tag_ids:
                tag = self.session.get(Tag, tag_id)
                if not tag or tag.user_id != user_id:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Tag with ID {tag_id} not found or doesn't belong to user"
                    )

        # Create the task
        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            completed=task_data.completed or False,
            category_id=task_data.category_id,
            due_date=task_data.due_date,
            priority=task_data.priority
        )

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        # Add tags to the task if provided
        if tag_ids:
            for tag_id in tag_ids:
                task_tag = TaskTag(task_id=task.id, tag_id=tag_id)
                self.session.add(task_tag)
            self.session.commit()

        return self._task_to_response(task)

    def get_tasks(
        self,
        user_id: int,
        status_filter: Optional[str] = None,
        category_id: Optional[int] = None,
        tag_ids: Optional[List[int]] = None,
        due_date_start: Optional[datetime] = None,
        due_date_end: Optional[datetime] = None,
        priority: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[TaskResponse]:
        """Get tasks for a user with optional filters"""
        query = select(Task).where(Task.user_id == user_id)

        # Apply filters
        if status_filter:
            if status_filter == "pending":
                query = query.where(Task.completed == False)
            elif status_filter == "completed":
                query = query.where(Task.completed == True)

        if category_id:
            query = query.where(Task.category_id == category_id)

        if due_date_start:
            query = query.where(Task.due_date >= due_date_start)
        if due_date_end:
            query = query.where(Task.due_date <= due_date_end)

        if priority:
            query = query.where(Task.priority == priority)

        # Apply sorting (default to created_at descending)
        query = query.order_by(Task.created_at.desc())

        # Apply limit and offset for pagination
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)

        tasks = self.session.exec(query).all()

        # Filter by tags if specified (requires additional processing)
        if tag_ids:
            filtered_tasks = []
            for task in tasks:
                task_tag_ids = [tt.tag_id for tt in task.task_tags]
                if all(tag_id in task_tag_ids for tag_id in tag_ids):
                    filtered_tasks.append(task)
            tasks = filtered_tasks

        return [self._task_to_response(task) for task in tasks]

    def get_task(self, user_id: int, task_id: int) -> TaskResponse:
        """Get a specific task for a user"""
        task = self.session.get(Task, task_id)
        if not task or task.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or doesn't belong to user"
            )

        return self._task_to_response(task)

    def update_task(self, user_id: int, task_id: int, task_data: TaskUpdate, tag_ids: Optional[List[int]] = None) -> TaskResponse:
        """Update a specific task for a user"""
        task = self.session.get(Task, task_id)
        if not task or task.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or doesn't belong to user"
            )

        # Verify category exists and belongs to user (if provided)
        if task_data.category_id is not None:
            if task_data.category_id:
                category = self.session.get(Category, task_data.category_id)
                if not category or category.user_id != user_id:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Category not found or doesn't belong to user"
                    )
            task.category_id = task_data.category_id

        # Verify tag IDs belong to user (if provided)
        if tag_ids:
            for tag_id in tag_ids:
                tag = self.session.get(Tag, tag_id)
                if not tag or tag.user_id != user_id:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Tag with ID {tag_id} not found or doesn't belong to user"
                    )

        # Update other fields if provided
        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.completed is not None:
            task.completed = task_data.completed
        if task_data.due_date is not None:
            task.due_date = task_data.due_date
        if task_data.priority is not None:
            task.priority = task_data.priority

        self.session.add(task)
        self.session.commit()

        # Update tags if provided
        if tag_ids is not None:
            # Remove existing tags
            existing_task_tags = self.session.exec(
                select(TaskTag).where(TaskTag.task_id == task_id)
            ).all()
            for task_tag in existing_task_tags:
                self.session.delete(task_tag)

            # Add new tags
            for tag_id in tag_ids:
                task_tag = TaskTag(task_id=task.id, tag_id=tag_id)
                self.session.add(task_tag)

            self.session.commit()

        self.session.refresh(task)

        return self._task_to_response(task)

    def delete_task(self, user_id: int, task_id: int) -> bool:
        """Delete a specific task for a user"""
        task = self.session.get(Task, task_id)
        if not task or task.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or doesn't belong to user"
            )

        self.session.delete(task)
        self.session.commit()
        return True

    def toggle_task_completion(self, user_id: int, task_id: int) -> TaskResponse:
        """Toggle the completion status of a task"""
        task = self.session.get(Task, task_id)
        if not task or task.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or doesn't belong to user"
            )

        task.completed = not task.completed
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        return self._task_to_response(task)

    def _task_to_response(self, task: Task) -> TaskResponse:
        """Convert Task model to TaskResponse with related data"""
        # Get the category if it exists
        category_response = None
        if task.category:
            category_response = {
                "id": task.category.id,
                "user_id": task.category.user_id,
                "name": task.category.name,
                "color": task.category.color,
                "created_at": task.category.created_at,
                "updated_at": task.category.updated_at
            }

        # Get the tags if they exist
        tag_responses = []
        for task_tag in task.task_tags:
            tag_responses.append({
                "id": task_tag.tag.id,
                "user_id": task_tag.tag.user_id,
                "name": task_tag.tag.name,
                "created_at": task_tag.tag.created_at,
                "updated_at": task_tag.tag.updated_at
            })

        return TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            category_id=task.category_id,
            due_date=task.due_date,
            priority=task.priority,
            created_at=task.created_at,
            updated_at=task.updated_at,
            category=category_response,
            tags=tag_responses
        )

    def add_tags_to_task(self, user_id: int, task_id: int, tag_ids: List[int]) -> TaskResponse:
        """Add tags to a specific task"""
        # Verify task exists and belongs to user
        task = self.session.get(Task, task_id)
        if not task or task.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or doesn't belong to user"
            )

        # Verify all tag IDs belong to user
        for tag_id in tag_ids:
            tag = self.session.get(Tag, tag_id)
            if not tag or tag.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Tag with ID {tag_id} not found or doesn't belong to user"
                )

        # Add tags that aren't already associated with the task
        for tag_id in tag_ids:
            existing_task_tag = self.session.exec(
                select(TaskTag)
                .where(TaskTag.task_id == task_id)
                .where(TaskTag.tag_id == tag_id)
            ).first()

            if not existing_task_tag:
                task_tag = TaskTag(task_id=task_id, tag_id=tag_id)
                self.session.add(task_tag)

        self.session.commit()
        self.session.refresh(task)

        return self._task_to_response(task)

    def remove_tags_from_task(self, user_id: int, task_id: int, tag_ids: List[int]) -> TaskResponse:
        """Remove tags from a specific task"""
        # Verify task exists and belongs to user
        task = self.session.get(Task, task_id)
        if not task or task.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or doesn't belong to user"
            )

        # Remove specified tags
        for tag_id in tag_ids:
            task_tag = self.session.exec(
                select(TaskTag)
                .where(TaskTag.task_id == task_id)
                .where(TaskTag.tag_id == tag_id)
            ).first()

            if task_tag:
                self.session.delete(task_tag)

        self.session.commit()
        self.session.refresh(task)

        return self._task_to_response(task)

    def search_tasks(
        self,
        user_id: int,
        search_query: Optional[str] = None,
        status_filter: Optional[str] = None,
        category_id: Optional[int] = None,
        tag_ids: Optional[List[int]] = None,
        due_date_start: Optional[datetime] = None,
        due_date_end: Optional[datetime] = None,
        priority: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = "asc",
        limit: Optional[int] = 20,
        offset: Optional[int] = 0
    ) -> List[TaskResponse]:
        """Search and filter tasks with advanced options"""
        # Start with base query that joins with TaskTag for tag filtering
        query = select(Task).where(Task.user_id == user_id)

        # Apply text search if query provided
        if search_query:
            query = query.where(
                Task.title.contains(search_query) |
                Task.description.contains(search_query)
            )

        # Apply filters
        if status_filter:
            if status_filter == "pending":
                query = query.where(Task.completed == False)
            elif status_filter == "completed":
                query = query.where(Task.completed == True)

        if category_id:
            query = query.where(Task.category_id == category_id)

        if due_date_start:
            query = query.where(Task.due_date >= due_date_start)
        if due_date_end:
            query = query.where(Task.due_date <= due_date_end)

        if priority:
            query = query.where(Task.priority == priority)

        # Apply sorting
        if sort_by == "title":
            if sort_order == "desc":
                query = query.order_by(Task.title.desc())
            else:
                query = query.order_by(Task.title.asc())
        elif sort_by == "due_date":
            if sort_order == "desc":
                query = query.order_by(Task.due_date.desc())
            else:
                query = query.order_by(Task.due_date.asc())
        elif sort_by == "priority":
            if sort_order == "desc":
                query = query.order_by(Task.priority.desc(), Task.created_at.desc())
            else:
                query = query.order_by(Task.priority.asc(), Task.created_at.desc())
        else:  # Default sort by creation date
            if sort_order == "desc":
                query = query.order_by(Task.created_at.desc())
            else:
                query = query.order_by(Task.created_at.asc())

        # Apply limit and offset for pagination
        query = query.limit(limit).offset(offset)

        # Execute the query
        tasks = self.session.exec(query).all()

        # Filter by tags if specified (requires additional processing)
        if tag_ids:
            filtered_tasks = []
            for task in tasks:
                task_tag_ids = [tt.tag_id for tt in task.task_tags]
                if all(tag_id in task_tag_ids for tag_id in tag_ids):
                    filtered_tasks.append(task)
            tasks = filtered_tasks

        return [self._task_to_response(task) for task in tasks]