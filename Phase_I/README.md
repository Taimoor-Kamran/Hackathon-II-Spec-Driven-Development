# Hackathon II: The Evolution of Todo

## Phase I: Todo In-Memory Python Console App

This is Phase I of the Hackathon II project: a command-line todo application that stores tasks in memory. Built with Python using Claude Code and Spec-Kit Plus following spec-driven development.

## Overview

The Evolution of Todo is a 5-phase project that takes a simple console application and evolves it into a fully-featured, cloud-native AI chatbot deployed on Kubernetes. This journey teaches the Nine Pillars of AI-Driven Development, Claude Code, Spec-Driven Development with Reusable Intelligence, and Cloud-Native AI technologies through hands-on implementation.

Phase I focuses on implementing the 5 Basic Level features:
1. Add Task – Create new todo items
2. Delete Task – Remove tasks from the list
3. Update Task – Modify existing task details
4. View Task List – Display all tasks
5. Mark as Complete – Toggle task completion status

## Requirements

- Python 3.13+
- UV package manager

## Installation

1. Clone the repository
2. Install dependencies using UV:
```bash
uv venv  # Create virtual environment
source .venv/bin/activate  # Activate virtual environment
uv pip install -e .  # Install the package in development mode
```

## Usage

Run the console application:
```bash
python -m src.main
```

### Available Commands
- `add "task title" "optional description"` - Add a new task
- `list` - Display all tasks
- `update <id> "new title" "new description"` - Update a task
- `delete <id>` - Delete a task
- `complete <id>` - Mark task as complete
- `incomplete <id>` - Mark task as incomplete
- `help` - Show available commands
- `quit` or `exit` - Exit the application

## Project Structure

```
todo-app/
├── src/                      # Source code
│   ├── __init__.py
│   ├── main.py               # Entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py           # Task model
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py   # Task operations
│   └── cli/
│       ├── __init__.py
│       └── console.py        # Console interface
├── specs/                    # Specification files
├── tests/                    # Test files
├── CLAUDE.md                 # Claude Code instructions
├── pyproject.toml            # Project configuration
└── README.md                 # This file
```

## Spec-Driven Development

This project follows the Spec-Driven Development workflow:
1. Constitution (/sp.constitution): Define/update project principles
2. Specify (/sp.specify): Create features specification with user stories
3. Clarify (/sp.clarify): Resolve ambiguities in specifications
4. Plan (/sp.plan): Generate technical implementation plan
5. Tasks (/sp.tasks): Break down into actionable, testable tasks
6. Implement (/sp.implement): Execute tasks using Red-Green-Refactor
7. Document (/sp.adr): Record architectural decisions when significant
8. Record (/sp.phr): Create prompt History Records for traceability

Specifications are located in the `/specs` directory.

## Phase Progression

- **Phase I**: Todo In-Memory Python Console App (Current)
- **Phase II**: Full-Stack Web Application
- **Phase III**: AI-Powered Todo Chatbot
- **Phase IV**: Local Kubernetes Deployment
- **Phase V**: Advanced Cloud Deployment