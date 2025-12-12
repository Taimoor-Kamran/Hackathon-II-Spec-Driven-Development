# Phase II: Todo Full-Stack Web Application - Specification

## Overview
This specification defines the requirements for Phase II of the Hackathon II project: transforming the Phase I console app into a modern multi-user web application with persistent storage. This phase focuses on implementing the 5 Basic Level features as a web application using Next.js, FastAPI, SQLModel, and Neon Serverless PostgreSQL.

## Objective
Using Claude Code and Spec-Kit Plus, transform the Phase I console app into a modern multi-user web application with persistent storage. The application must implement all 5 Basic Level features as a web application with RESTful API endpoints, responsive frontend interface, Neon Serverless PostgreSQL database, and authentication using Better Auth.

## User Stories

### As a user, I want to create an account and log in
- Given I am a new user
- When I visit the application
- Then I can create an account and log in
- And my data will be isolated from other users

### As a logged-in user, I want to add tasks via the web interface
- Given I am logged in
- When I enter a new task in the web form
- Then the task should be created and stored in the database
- And I should receive confirmation that the task was added

### As a logged-in user, I want to view my tasks via the web interface
- Given I am logged in and have tasks in my todo list
- When I navigate to the tasks page
- Then all my tasks should be displayed with their status indicators
- And each task should show its ID, title, description, and completion status

### As a logged-in user, I want to update task details via the web interface
- Given I am logged in and have tasks in my todo list
- When I edit a specific task via the web interface
- Then the task details should be modified in the database
- And I should receive confirmation of the update

### As a logged-in user, I want to delete tasks via the web interface
- Given I am logged in and have tasks in my todo list
- When I delete a specific task via the web interface
- Then the task should be removed from the database
- And I should receive confirmation that the task was deleted

### As a logged-in user, I want to mark tasks as complete/incomplete via the web interface
- Given I am logged in and have tasks in my todo list
- When I toggle the completion status of a specific task via the web interface
- Then the task's completion status should be updated in the database
- And I should receive confirmation of the status change

## Functional Requirements

### FREQ-001: User Authentication
- The application must provide user signup functionality
- The application must provide user login functionality
- The application must provide user logout functionality
- The application must use Better Auth with JWT tokens
- All API requests must include a valid JWT token in the Authorization header
- The application must verify JWT tokens and extract user information
- Each user should only see their own tasks

### FREQ-002: Add Task via API
- The application must expose a POST /api/{user_id}/tasks endpoint
- The endpoint must accept a JSON payload with title (required) and description (optional)
- The endpoint must validate that the title is 1-200 characters
- The endpoint must validate that the description is max 1000 characters if provided
- The endpoint must create a new task in the database associated with the user
- The endpoint must return the created task object with all details
- The endpoint must require a valid JWT token
- The endpoint must verify that the user_id in the URL matches the authenticated user

### FREQ-003: List Tasks via API
- The application must expose a GET /api/{user_id}/tasks endpoint
- The endpoint must return an array of task objects for the authenticated user
- The endpoint must support query parameters: status (all|pending|completed), sort (created|title|due_date)
- The endpoint must return task objects with id, title, description, completed, created_at, updated_at
- The endpoint must require a valid JWT token
- The endpoint must verify that the user_id in the URL matches the authenticated user

### FREQ-004: Get Task via API
- The application must expose a GET /api/{user_id}/tasks/{id} endpoint
- The endpoint must return a single task object with all details
- The endpoint must validate that the task belongs to the authenticated user
- The endpoint must return 404 if the task doesn't exist
- The endpoint must require a valid JWT token
- The endpoint must verify that the user_id in the URL matches the authenticated user

### FREQ-005: Update Task via API
- The application must expose a PUT /api/{user_id}/tasks/{id} endpoint
- The endpoint must accept a JSON payload with title and/or description
- The endpoint must validate the input data (title length, description length)
- The endpoint must update the task in the database
- The endpoint must return the updated task object
- The endpoint must require a valid JWT token
- The endpoint must verify that the user_id in the URL matches the authenticated user
- The endpoint must verify that the task belongs to the authenticated user

### FREQ-006: Delete Task via API
- The application must expose a DELETE /api/{user_id}/tasks/{id} endpoint
- The endpoint must delete the task from the database
- The endpoint must return a success response
- The endpoint must return 404 if the task doesn't exist
- The endpoint must require a valid JWT token
- The endpoint must verify that the user_id in the URL matches the authenticated user
- The endpoint must verify that the task belongs to the authenticated user

### FREQ-007: Complete Task via API
- The application must expose a PATCH /api/{user_id}/tasks/{id}/complete endpoint
- The endpoint must toggle the completion status of the task
- The endpoint must return the updated task object
- The endpoint must return 404 if the task doesn't exist
- The endpoint must require a valid JWT token
- The endpoint must verify that the user_id in the URL matches the authenticated user
- The endpoint must verify that the task belongs to the authenticated user

### FREQ-008: Frontend Interface
- The application must provide a responsive web interface using Next.js
- The interface must include pages for login/signup, task list, and task management
- The interface must display all tasks for the logged-in user
- The interface must allow adding, updating, deleting, and completing tasks
- The interface must handle authentication state
- The interface must display appropriate feedback for all operations

## Non-Functional Requirements

### NFR-001: Performance
- API endpoints should respond within 2 seconds
- Database queries should be optimized
- Frontend should load within 3 seconds on average connection
- Pagination should be implemented for large task lists

### NFR-002: Security
- All API endpoints must require authentication
- User data must be properly isolated
- JWT tokens must be properly validated
- Input must be validated and sanitized
- SQL injection must be prevented through ORM usage

### NFR-003: Usability
- The web interface should be intuitive and responsive
- Error messages should be clear and helpful
- The application should provide loading states for operations
- The interface should work on desktop and mobile devices

### NFR-004: Reliability
- The application should handle network errors gracefully
- The application should provide offline indicators
- Database operations should be atomic where appropriate
- The application should maintain data consistency

## Technical Requirements

### Technology Stack
- Frontend: Next.js 16+ with App Router
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT
- Claude Code for implementation

### Project Structure
```
phase2-todo/
├── .spec-kit/                    # Spec-Kit configuration
├── specs/                        # Specification files
│   ├── phase2-overview.md
│   ├── phase2-features/
│   │   ├── task-crud.md
│   │   ├── authentication.md
│   │   └── frontend-pages.md
│   ├── phase2-architecture.md
│   └── phase2-api.md
├── frontend/                     # Next.js frontend
│   ├── app/                      # App Router pages
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── login/
│   │   ├── signup/
│   │   └── dashboard/
│   ├── components/               # Reusable components
│   ├── lib/                      # Utilities and API client
│   ├── styles/                   # CSS styles
│   ├── CLAUDE.md                 # Frontend Claude instructions
│   └── package.json
├── backend/                      # FastAPI backend
│   ├── main.py                   # FastAPI app entry point
│   ├── models.py                 # SQLModel database models
│   ├── routes/                   # API route handlers
│   │   ├── auth.py
│   │   └── tasks.py
│   ├── database.py               # Database connection
│   ├── auth.py                   # Authentication utilities
│   ├── CLAUDE.md                 # Backend Claude instructions
│   └── requirements.txt
├── CLAUDE.md                     # Root Claude Code instructions
└── README.md                     # Documentation
```

### Database Schema
- **users** table (managed by Better Auth):
  - id: string (primary key)
  - email: string (unique)
  - name: string
  - created_at: timestamp

- **tasks** table:
  - id: integer (primary key, auto-increment)
  - user_id: string (foreign key → users.id)
  - title: string (not null, 1-200 characters)
  - description: text (nullable, max 1000 characters)
  - completed: boolean (default false)
  - created_at: timestamp
  - updated_at: timestamp

### API Endpoints
- **Authentication** (handled by Better Auth)
  - POST /api/auth/signup
  - POST /api/auth/login
  - POST /api/auth/logout

- **Tasks API**
  - GET /api/{user_id}/tasks - List all tasks
  - POST /api/{user_id}/tasks - Create a new task
  - GET /api/{user_id}/tasks/{id} - Get task details
  - PUT /api/{user_id}/tasks/{id} - Update a task
  - DELETE /api/{user_id}/tasks/{id} - Delete a task
  - PATCH /api/{user_id}/tasks/{id}/complete - Toggle completion

### Frontend Pages
- `/` - Landing page with login/signup options
- `/login` - User login form
- `/signup` - User registration form
- `/dashboard` - Main task management interface
- `/tasks/[id]` - Individual task view (optional)

## Acceptance Criteria

### AC-001: Authentication Implementation
- [ ] Users can create accounts via signup form
- [ ] Users can log in with existing credentials
- [ ] JWT tokens are properly issued and validated
- [ ] API requests include Authorization header with Bearer token
- [ ] Users are properly isolated (can't see others' tasks)

### AC-002: Task Creation API
- [ ] POST /api/{user_id}/tasks endpoint works correctly
- [ ] Task creation validates input properly
- [ ] Created tasks are stored in database
- [ ] Response includes complete task object
- [ ] Authentication is required and validated

### AC-003: Task Listing API
- [ ] GET /api/{user_id}/tasks endpoint works correctly
- [ ] Only returns tasks for authenticated user
- [ ] Supports query parameters for filtering and sorting
- [ ] Returns properly formatted task objects
- [ ] Authentication is required and validated

### AC-004: Task Retrieval API
- [ ] GET /api/{user_id}/tasks/{id} endpoint works correctly
- [ ] Returns single task object with all details
- [ ] Returns 404 for non-existent tasks
- [ ] Validates task ownership
- [ ] Authentication is required and validated

### AC-005: Task Update API
- [ ] PUT /api/{user_id}/tasks/{id} endpoint works correctly
- [ ] Updates task in database
- [ ] Validates input data
- [ ] Returns updated task object
- [ ] Authentication is required and validated

### AC-006: Task Deletion API
- [ ] DELETE /api/{user_id}/tasks/{id} endpoint works correctly
- [ ] Removes task from database
- [ ] Returns success response
- [ ] Returns 404 for non-existent tasks
- [ ] Authentication is required and validated

### AC-007: Task Completion API
- [ ] PATCH /api/{user_id}/tasks/{id}/complete endpoint works correctly
- [ ] Toggles completion status in database
- [ ] Returns updated task object
- [ ] Returns 404 for non-existent tasks
- [ ] Authentication is required and validated

### AC-008: Frontend Interface
- [ ] Responsive design works on desktop and mobile
- [ ] All 5 Basic Level operations available via UI
- [ ] Proper feedback for all operations
- [ ] Authentication state is maintained
- [ ] Tasks are displayed with proper status indicators

## Error Handling
- API endpoints return appropriate HTTP status codes
- Frontend displays user-friendly error messages
- Validation errors are properly handled
- Authentication failures are handled gracefully
- Database errors are caught and handled appropriately