from sqlmodel import Session, select
from typing import List
from datetime import datetime, timedelta
from models import Task, User, TaskResponse, TaskTag, Category

class AIService:
    def __init__(self, session: Session):
        self.session = session

    def get_task_suggestions(self, user_id: int, limit: int = 5) -> List[TaskResponse]:
        """
        Generate AI-powered task suggestions based on user's historical data.
        This is a rule-based system that analyzes patterns in completed tasks.
        """
        # Get user's completed tasks from the last 90 days
        cutoff_date = datetime.now() - timedelta(days=90)

        completed_tasks = self.session.exec(
            select(Task)
            .where(Task.user_id == user_id)
            .where(Task.completed == True)
            .where(Task.created_at >= cutoff_date)
        ).all()

        suggestions = []

        # Analyze patterns in completed tasks
        title_patterns = {}
        category_patterns = {}
        tag_patterns = {}
        day_patterns = {}

        for task in completed_tasks:
            # Count title patterns
            if task.title.lower() in title_patterns:
                title_patterns[task.title.lower()] += 1
            else:
                title_patterns[task.title.lower()] = 1

            # Count categories
            if task.category_id:
                if task.category_id in category_patterns:
                    category_patterns[task.category_id] += 1
                else:
                    category_patterns[task.category_id] = 1

            # Count tags
            for task_tag in task.task_tags:
                tag_id = task_tag.tag_id
                if tag_id in tag_patterns:
                    tag_patterns[tag_id] += 1
                else:
                    tag_patterns[tag_id] = 1

            # Count day patterns (day of week)
            day_of_week = task.created_at.weekday()  # 0=Monday, 6=Sunday
            if day_of_week in day_patterns:
                day_patterns[day_of_week] += 1
            else:
                day_patterns[day_of_week] = 1

        # Generate suggestions based on patterns
        for title, count in sorted(title_patterns.items(), key=lambda x: x[1], reverse=True)[:limit]:
            if count > 1:  # Only suggest tasks that were completed multiple times
                # Create a suggested task based on the pattern
                suggested_task = TaskResponse(
                    id=0,  # Placeholder ID
                    title=title,
                    description=f"Suggested task based on your previous work",
                    completed=False,
                    user_id=user_id,
                    category_id=None,  # Will be set when user creates the task
                    due_date=None,  # User will set this
                    priority="medium",
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    category=None,
                    tags=[]
                )
                suggestions.append(suggested_task)

        # If we don't have enough suggestions from title patterns, add some based on categories
        if len(suggestions) < limit:
            for category_id, count in sorted(category_patterns.items(), key=lambda x: x[1], reverse=True):
                if len(suggestions) >= limit:
                    break

                # Find a representative task from this category to suggest
                category_task = self.session.exec(
                    select(Task)
                    .where(Task.user_id == user_id)
                    .where(Task.category_id == category_id)
                    .where(Task.completed == True)
                    .order_by(Task.updated_at.desc())
                    .limit(1)
                ).first()

                if category_task and category_task.title.lower() not in [s.title.lower() for s in suggestions]:
                    suggested_task = TaskResponse(
                        id=0,
                        title=f"Follow-up to {category_task.title}",
                        description=f"Related to your work in the {category_task.category.name if category_task.category else 'a specific area'}",
                        completed=False,
                        user_id=user_id,
                        category_id=category_id,
                        due_date=None,
                        priority="medium",
                        created_at=datetime.now(),
                        updated_at=datetime.now(),
                        category=None,
                        tags=[]
                    )
                    suggestions.append(suggested_task)

        # If we still don't have enough suggestions, add some based on tags
        if len(suggestions) < limit:
            for tag_id, count in sorted(tag_patterns.items(), key=lambda x: x[1], reverse=True):
                if len(suggestions) >= limit:
                    break

                # Find a representative task with this tag to suggest
                tag_task = self.session.exec(
                    select(Task)
                    .join(TaskTag)
                    .where(Task.user_id == user_id)
                    .where(TaskTag.tag_id == tag_id)
                    .where(Task.completed == True)
                    .order_by(Task.updated_at.desc())
                    .limit(1)
                ).first()

                if tag_task and tag_task.title.lower() not in [s.title.lower() for s in suggestions]:
                    suggested_task = TaskResponse(
                        id=0,
                        title=f"Related to {tag_task.title}",
                        description=f"Related to your work tagged with {tag_task.task_tags[0].tag.name if tag_task.task_tags else 'a specific tag'}",
                        completed=False,
                        user_id=user_id,
                        category_id=tag_task.category_id,
                        due_date=None,
                        priority="medium",
                        created_at=datetime.now(),
                        updated_at=datetime.now(),
                        category=None,
                        tags=[]
                    )
                    suggestions.append(suggested_task)

        # Limit to the requested number
        return suggestions[:limit]

    def analyze_user_patterns(self, user_id: int):
        """
        Analyze user's task patterns to provide insights.
        This could be used for more sophisticated suggestions in the future.
        """
        # Get all tasks for the user
        all_tasks = self.session.exec(
            select(Task)
            .where(Task.user_id == user_id)
        ).all()

        stats = {
            "total_tasks": len(all_tasks),
            "completed_tasks": len([t for t in all_tasks if t.completed]),
            "pending_tasks": len([t for t in all_tasks if not t.completed]),
        }

        # Analyze completion patterns
        completion_times = []
        for task in all_tasks:
            if task.completed and task.created_at and task.updated_at:
                completion_times.append((task.updated_at - task.created_at).total_seconds())

        if completion_times:
            avg_completion_time = sum(completion_times) / len(completion_times)
            stats["avg_completion_time_seconds"] = avg_completion_time
            stats["avg_completion_time_hours"] = avg_completion_time / 3600

        return stats