#!/usr/bin/env python3
"""
MCP Server for Todo AI Chatbot
Exposes task operations as tools for AI agents
"""

import asyncio
import json
from typing import Dict, Any, List
from mcp.server import Server
from mcp.types import (
    ClientCapabilities,
    InitializeRequest,
    InitializeResult,
    Tool,
    CallToolResult,
    ListToolsResult,
)
from sqlmodel import SQLModel, Field, create_engine, Session, select
from datetime import datetime
import os


# Database Models
class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: str
    title: str
    description: str = None
    completed: bool = False
    category_id: int = None
    due_date: str = None
    priority: str = "medium"
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Category(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: str
    name: str
    color: str = "#000000"
    created_at: datetime = Field(default_factory=datetime.now)


class Tag(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: str
    name: str
    created_at: datetime = Field(default_factory=datetime.now)


# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///todo_phase_iii.db")
engine = create_engine(DATABASE_URL, echo=False)  # Disable SQL logging to stdout


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Create the server
server = Server(
    name="todo-ai-chatbot-mcp",
    version="1.0.0",
    instructions="This server provides tools for managing tasks, categories, and tags for a todo application."
)


# Define tools that the server provides
@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """Return the list of available tools."""
    tools = [
        Tool(
            name="list_tasks",
            description="List all tasks for a user",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user ID"}
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="create_task",
            description="Create a new task",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user ID"},
                    "title": {"type": "string", "description": "The title of the task"},
                    "description": {"type": "string", "description": "Optional description of the task"},
                    "category_id": {"type": "integer", "description": "Optional category ID"},
                    "due_date": {"type": "string", "description": "Optional due date in YYYY-MM-DD format"},
                    "priority": {"type": "string", "description": "Priority level (low, medium, high)"}
                },
                "required": ["user_id", "title"]
            }
        ),
        Tool(
            name="update_task",
            description="Update an existing task",
            input_schema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "The ID of the task to update"},
                    "user_id": {"type": "string", "description": "The user ID"},
                    "title": {"type": "string", "description": "New title (optional)"},
                    "description": {"type": "string", "description": "New description (optional)"},
                    "completed": {"type": "boolean", "description": "New completion status (optional)"},
                    "category_id": {"type": "integer", "description": "New category ID (optional)"},
                    "due_date": {"type": "string", "description": "New due date (optional)"},
                    "priority": {"type": "string", "description": "New priority level (optional)"}
                },
                "required": ["task_id", "user_id"]
            }
        ),
        Tool(
            name="delete_task",
            description="Delete a task",
            input_schema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "The ID of the task to delete"},
                    "user_id": {"type": "string", "description": "The user ID"}
                },
                "required": ["task_id", "user_id"]
            }
        ),
        Tool(
            name="list_categories",
            description="List all categories for the user",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user ID"}
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="create_category",
            description="Create a new category",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user ID"},
                    "name": {"type": "string", "description": "The name of the category"},
                    "color": {"type": "string", "description": "Hex color code for the category"}
                },
                "required": ["user_id", "name"]
            }
        ),
        Tool(
            name="list_tags",
            description="List all tags for the user",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user ID"}
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="create_tag",
            description="Create a new tag",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user ID"},
                    "name": {"type": "string", "description": "The name of the tag"}
                },
                "required": ["user_id", "name"]
            }
        )
    ]
    return ListToolsResult(tools=tools)


# Handle tool calls
@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls by executing the appropriate function."""
    try:
        if name == "list_tasks":
            result = await list_tasks(arguments["user_id"])
        elif name == "create_task":
            result = await create_task(
                user_id=arguments["user_id"],
                title=arguments["title"],
                description=arguments.get("description"),
                category_id=arguments.get("category_id"),
                due_date=arguments.get("due_date"),
                priority=arguments.get("priority", "medium")
            )
        elif name == "update_task":
            result = await update_task(
                task_id=arguments["task_id"],
                user_id=arguments["user_id"],
                title=arguments.get("title"),
                description=arguments.get("description"),
                completed=arguments.get("completed"),
                category_id=arguments.get("category_id"),
                due_date=arguments.get("due_date"),
                priority=arguments.get("priority")
            )
        elif name == "delete_task":
            result = await delete_task(
                task_id=arguments["task_id"],
                user_id=arguments["user_id"]
            )
        elif name == "list_categories":
            result = await list_categories(arguments["user_id"])
        elif name == "create_category":
            result = await create_category(
                user_id=arguments["user_id"],
                name=arguments["name"],
                color=arguments.get("color", "#000000")
            )
        elif name == "list_tags":
            result = await list_tags(arguments["user_id"])
        elif name == "create_tag":
            result = await create_tag(
                user_id=arguments["user_id"],
                name=arguments["name"]
            )
        else:
            return CallToolResult(content=[
                {"type": "text", "text": f"Unknown tool: {name}"}
            ])

        return CallToolResult(content=[
            {"type": "text", "text": json.dumps(result)}
        ])
    except Exception as e:
        return CallToolResult(content=[
            {"type": "text", "text": f"Error calling tool {name}: {str(e)}"}
        ])


# Database functions
async def list_tasks(user_id: str) -> List[Dict[str, Any]]:
    """List all tasks for a user."""
    with Session(engine) as session:
        tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
        return [{"id": task.id, "title": task.title, "completed": task.completed,
                 "description": task.description, "category_id": task.category_id,
                 "due_date": task.due_date, "priority": task.priority} for task in tasks]


async def create_task(user_id: str, title: str, description: str = None,
                    category_id: int = None, due_date: str = None,
                    priority: str = "medium") -> Dict[str, Any]:
    """Create a new task."""
    with Session(engine) as session:
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            category_id=category_id,
            due_date=due_date,
            priority=priority
        )
        session.add(task)
        session.commit()
        session.refresh(task)

        return {"id": task.id, "title": task.title, "completed": task.completed,
                "description": task.description, "category_id": task.category_id,
                "due_date": task.due_date, "priority": task.priority}


async def update_task(task_id: int, user_id: str, title: str = None,
                    description: str = None, completed: bool = None,
                    category_id: int = None, due_date: str = None,
                    priority: str = None) -> Dict[str, Any]:
    """Update an existing task."""
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            raise ValueError(f"Task {task_id} not found or not owned by user {user_id}")

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed
        if category_id is not None:
            task.category_id = category_id
        if due_date is not None:
            task.due_date = due_date
        if priority is not None:
            task.priority = priority

        task.updated_at = datetime.now()
        session.add(task)
        session.commit()
        session.refresh(task)

        return {"id": task.id, "title": task.title, "completed": task.completed,
                "description": task.description, "category_id": task.category_id,
                "due_date": task.due_date, "priority": task.priority}


async def delete_task(task_id: int, user_id: str) -> Dict[str, str]:
    """Delete a task."""
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            raise ValueError(f"Task {task_id} not found or not owned by user {user_id}")

        session.delete(task)
        session.commit()

        return {"message": f"Task {task_id} deleted successfully"}


async def list_categories(user_id: str) -> List[Dict[str, Any]]:
    """List all categories for a user."""
    with Session(engine) as session:
        categories = session.exec(select(Category).where(Category.user_id == user_id)).all()
        return [{"id": cat.id, "name": cat.name, "color": cat.color} for cat in categories]


async def create_category(user_id: str, name: str, color: str = "#000000") -> Dict[str, Any]:
    """Create a new category."""
    with Session(engine) as session:
        category = Category(user_id=user_id, name=name, color=color)
        session.add(category)
        session.commit()
        session.refresh(category)

        return {"id": category.id, "name": category.name, "color": category.color}


async def list_tags(user_id: str) -> List[Dict[str, Any]]:
    """List all tags for a user."""
    with Session(engine) as session:
        tags = session.exec(select(Tag).where(Tag.user_id == user_id)).all()
        return [{"id": tag.id, "name": tag.name} for tag in tags]


async def create_tag(user_id: str, name: str) -> Dict[str, Any]:
    """Create a new tag."""
    with Session(engine) as session:
        tag = Tag(user_id=user_id, name=name)
        session.add(tag)
        session.commit()
        session.refresh(tag)

        return {"id": tag.id, "name": tag.name}


# Initialize database
create_db_and_tables()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8080

    from mcp import stdio_server

    # Run the server using stdio (don't print to stdout when in stdio mode)
    # Only print to stderr or not at all when using stdio_server
    stdio_server(server)