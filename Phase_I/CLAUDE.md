# Todo App - Hackathon II - Phase I

## Project Overview
This is Phase I of the Hackathon II project: a command-line todo application that stores tasks in memory. Built with Python using Claude Code and Spec-Kit Plus following spec-driven development.

## Spec-Kit Structure
Specifications are organized in /specs:
- /specs/phase1-overview.md - Project overview
- /specs/phase1-features/ - Feature specs (what to build)
- /specs/phase1-architecture.md - System architecture

## How to Use Specs
1. Always read relevant spec before implementing
2. Reference specs with: @specs/phase1-features/task-crud.md
3. Update specs if requirements change

## Project Structure
- /src - Python source code
- /specs - Specification files
- /tests - Test files (to be created)

## Development Workflow
1. Read spec: @specs/phase1-features/[feature].md
2. Implement using clean architecture principles
3. Test and iterate

## Phase I Requirements
- Implement all 5 Basic Level features (Add, Delete, Update, View, Mark Complete)
- Use in-memory storage
- Create clean Python project structure
- Follow PEP 8 standards
- Include proper error handling

## Commands to Implement
- add "title" "description" - Add new task
- list - List all tasks
- update <id> "title" "description" - Update task
- delete <id> - Delete task
- complete <id> - Mark task complete
- incomplete <id> - Mark task incomplete
- help - Show help
- quit/exit - Exit app