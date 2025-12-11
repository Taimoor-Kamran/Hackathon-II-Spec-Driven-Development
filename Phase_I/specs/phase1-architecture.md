# Phase I Architecture: In-Memory Python Console App

## System Overview
The Phase I Todo application is a command-line interface application built in Python that stores tasks in memory. The application follows a clean architecture pattern with separation of concerns between data models, business logic, and user interface.

## Architecture Layers

### 1. Data Layer (Models)
- **Task Model**: Represents a single todo task with properties:
  - id: integer (auto-generated)
  - title: string (1-200 characters)
  - description: string (max 1000 characters, optional)
  - completed: boolean (default: false)
  - created_at: datetime
  - updated_at: datetime

### 2. Service Layer (Business Logic)
- **Task Service**: Handles all business operations for tasks:
  - Add task
  - Get all tasks
  - Get task by ID
  - Update task
  - Delete task
  - Mark task complete/incomplete
  - Validation logic

### 3. Interface Layer (CLI)
- **Console Interface**: Handles user input/output:
  - Command parsing
  - User prompts
  - Display formatting
  - Error messages
  - Help system

### 4. Storage Layer (In-Memory)
- **In-Memory Storage**: Uses Python data structures:
  - List or dictionary to store Task objects
  - Simple in-memory persistence (no file/database)

## Component Structure

```
src/
├── main.py              # Application entry point
├── models/
│   └── task.py          # Task data model
├── services/
│   └── task_service.py  # Business logic layer
└── cli/
    └── console.py       # Command-line interface
```

## Entry Point (main.py)
- Initializes the console interface
- Starts the command loop
- Handles application lifecycle

## Data Model (models/task.py)
- Defines the Task class
- Includes validation methods
- Handles timestamp management

## Service Layer (services/task_service.py)
- Implements all task operations
- Validates inputs
- Manages in-memory storage
- Returns appropriate responses

## Console Interface (cli/console.py)
- Parses user commands
- Calls appropriate service methods
- Formats and displays output
- Handles errors and edge cases

## Dependencies
- Python 3.13+
- Standard library only (no external dependencies for Phase I)

## In-Memory Storage Implementation
- Uses Python list/dict to store Task objects
- Maintains data during application runtime
- Data is lost when application exits (Phase I requirement)

## Error Handling Strategy
- Input validation at the CLI layer
- Business logic validation in service layer
- User-friendly error messages
- Graceful degradation for edge cases

## Command Flow
1. User enters command in console
2. CLI parses command and arguments
3. CLI calls appropriate service method
4. Service performs operation on in-memory data
5. Service returns result to CLI
6. CLI formats and displays result to user

## Testing Considerations
- Unit tests for Task model
- Unit tests for TaskService methods
- Integration tests for CLI functionality
- Mock in-memory storage for testing