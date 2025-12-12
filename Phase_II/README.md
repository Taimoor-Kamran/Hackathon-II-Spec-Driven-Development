# Phase II: Todo Full-Stack Web Application

This is Phase II of the Hackathon II project: transforming the Phase I console app into a modern multi-user web application with persistent storage using Next.js, FastAPI, SQLModel, and Neon Serverless PostgreSQL.

## Overview

Phase II implements a full-stack web application with:
- Frontend: Next.js 16+ with App Router
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT

## Features

All 5 Basic Level features are implemented:
1. Add Task – Create new todo items
2. Delete Task – Remove tasks from the list
3. Update Task – Modify existing task details
4. View Task List – Display all tasks
5. Mark as Complete – Toggle task completion status

## Architecture

The application follows a client-server architecture with JWT-based authentication for secure user isolation.

### Backend (FastAPI)
- REST API endpoints with proper authentication
- SQLModel for database operations
- JWT token validation middleware
- User isolation (each user sees only their tasks)

### Frontend (Next.js)
- Responsive web interface
- Task management components
- Authentication state management
- API client with JWT token handling

## API Endpoints

- `GET /api/{user_id}/tasks` - List user's tasks
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion

## Setup

### Backend Setup
1. Navigate to the backend directory: `cd Phase_II/backend`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in `.env`
4. Run the application: `uvicorn main:app --reload`

### Frontend Setup
1. Navigate to the frontend directory: `cd Phase_II/frontend`
2. Install dependencies: `npm install`
3. Run the development server: `npm run dev`

## Security

- JWT tokens for authentication
- User ID validation in URL matches authenticated user
- Input validation and sanitization
- SQL injection prevention through ORM

## Development Workflow

This project follows the Spec-Driven Development workflow:
1. Constitution (/sp.constitution): Define/update project principles
2. Specify (/sp.specify): Create features specification with user stories
3. Clarify (/sp.clarify): Resolve ambiguities in specifications
4. Plan (/sp.plan): Generate technical implementation plan
5. Tasks (/sp.tasks): Break down into actionable, testable tasks
6. Implement (/sp.implement): Execute tasks using Red-Green-Refactor
7. Document (/sp.adr): Record architectural decisions when significant
8. Record (/sp.phr): Create prompt History Records for traceability