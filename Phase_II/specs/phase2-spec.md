# Phase II: Todo Full-Stack Web Application - Specification

## Overview
This specification defines the requirements for Phase II of the Hackathon II project: transforming the Phase I console app into a modern multi-user web application with persistent storage. This phase focuses on implementing the 5 Basic Level features as a web application using Next.js, FastAPI, SQLModel, and SQLite database with JWT-based authentication. The application features complete user authentication, task management, and proper user isolation.

## Objective
Using Claude Code and Spec-Kit Plus, transform the Phase I console app into a modern multi-user web application with persistent storage. The application must implement all 5 Basic Level features as a web application with RESTful API endpoints, responsive frontend interface, SQLite database for local development (with PostgreSQL compatibility), and JWT-based authentication with bcrypt password hashing. Includes proper user isolation, input field fixes, and password validation (6-72 character limit due to bcrypt limitation).

## User Stories

### As a user, I want to create an account and log in
- Given I am a new user
- When I visit the application
- Then I can create an account with email, name, and password (6-72 characters)
- And I can log in with my credentials
- And my data will be isolated from other users

### As a logged-in user, I want to add tasks via the web interface
- Given I am logged in
- When I enter a new task in the web form
- Then the task should be created and stored in the database
- And I should receive confirmation that the task was added
- And the input field should properly display text as I type

### As a logged-in user, I want to view my tasks via the web interface
- Given I am logged in and have tasks in my todo list
- When I navigate to the dashboard
- Then all my tasks should be displayed with their status indicators
- And each task should show its ID, title, description, and completion status
- And tasks should persist across page refreshes

### As a logged-in user, I want to update task details via the web interface
- Given I am logged in and have tasks in my todo list
- When I edit a specific task via the web interface
- Then the task details should be modified in the database
- And I should receive confirmation of the update
- And changes should be reflected immediately

### As a logged-in user, I want to delete tasks via the web interface
- Given I am logged in and have tasks in my todo list
- When I delete a specific task via the web interface
- Then the task should be removed from the database
- And I should receive confirmation that the task was deleted
- And the task should disappear from the UI immediately

### As a logged-in user, I want to mark tasks as complete/incomplete via the web interface
- Given I am logged in and have tasks in my todo list
- When I toggle the completion status of a specific task via the web interface
- Then the task's completion status should be updated in the database
- And I should receive confirmation of the status change
- And the change should be reflected immediately in the UI

## Functional Requirements

### FREQ-001: User Authentication
- The application must provide user signup functionality with email, name, and password validation (6-72 characters)
- The application must provide user login functionality with JWT token generation
- The application must provide user logout functionality by clearing the token
- The application must use JWT-based authentication with bcrypt password hashing
- All API requests must include a valid JWT token in the Authorization header
- The application must verify JWT tokens and extract user information from database
- Each user should only see their own tasks with user_id validation

### FREQ-002: Add Task via API
- The application must expose a POST /api/{user_id}/tasks endpoint
- The endpoint must accept a JSON payload with title (required) and description (optional)
- The endpoint must validate that the title is 1-200 characters
- The endpoint must validate that the description is max 1000 characters if provided
- The endpoint must create a new task in the database associated with the user
- The endpoint must return the created task object with all details
- The endpoint must require a valid JWT token
- The endpoint must verify that the user_id in the URL matches the authenticated user_id

### FREQ-003: List Tasks via API
- The application must expose a GET /api/{user_id}/tasks endpoint
- The endpoint must return an array of task objects for the authenticated user
- The endpoint must support query parameters: status (all|pending|completed), sort (created|title|due_date)
- The endpoint must return task objects with id, title, description, completed, created_at, updated_at
- The endpoint must require a valid JWT token
- The endpoint must verify that the user_id in the URL matches the authenticated user_id

### FREQ-004: Get Task via API
- The application must expose a GET /api/{user_id}/tasks/{task_id} endpoint
- The endpoint must return a single task object with all details
- The endpoint must validate that the task belongs to the authenticated user
- The endpoint must return 404 if the task doesn't exist
- The endpoint must require a valid JWT token
- The endpoint must verify that the user_id in the URL matches the authenticated user_id

### FREQ-005: Update Task via API
- The application must expose a PUT /api/{user_id}/tasks/{task_id} endpoint
- The endpoint must accept a JSON payload with title and/or description
- The endpoint must validate the input data (title length, description length)
- The endpoint must update the task in the database
- The endpoint must return the updated task object
- The endpoint must require a valid JWT token
- The endpoint must verify that the user_id in the URL matches the authenticated user_id
- The endpoint must verify that the task belongs to the authenticated user

### FREQ-006: Delete Task via API
- The application must expose a DELETE /api/{user_id}/tasks/{task_id} endpoint
- The endpoint must delete the task from the database
- The endpoint must return a success response
- The endpoint must return 404 if the task doesn't exist
- The endpoint must require a valid JWT token
- The endpoint must verify that the user_id in the URL matches the authenticated user_id
- The endpoint must verify that the task belongs to the authenticated user

### FREQ-007: Complete Task via API
- The application must expose a PATCH /api/{user_id}/tasks/{task_id}/complete endpoint
- The endpoint must toggle the completion status of the task
- The endpoint must return the updated task object
- The endpoint must return 404 if the task doesn't exist
- The endpoint must require a valid JWT token
- The endpoint must verify that the user_id in the URL matches the authenticated user_id
- The endpoint must verify that the task belongs to the authenticated user

### FREQ-008: Frontend Interface
- The application must provide a responsive web interface using Next.js 16+ with App Router
- The interface must include pages for landing, login, signup, and dashboard
- The interface must display all tasks for the logged-in user with proper loading states
- The interface must allow adding, updating, deleting, and completing tasks
- The interface must handle authentication state with JWT token storage in localStorage
- The interface must display appropriate feedback for all operations
- The interface must fix input field issue so text properly appears when typing

### FREQ-009: Authentication API
- The application must expose a POST /auth/register endpoint for user registration
- The endpoint must validate email format, name length, and password length (6-72 characters)
- The endpoint must hash passwords with bcrypt and store user in database
- The application must expose a POST /auth/login endpoint for user login
- The endpoint must validate credentials and return JWT token
- The application must expose a GET /auth/me endpoint for current user info
- The endpoint must validate JWT token and return user information
- The authentication system must implement JWT-based authentication with proper token validation and expiration
- Passwords must be securely hashed using bcrypt with appropriate salt

## Non-Functional Requirements

### NFR-001: Performance
- API endpoints should respond within 2 seconds
- Database queries should be optimized
- Frontend should load within 3 seconds on average connection
- Pagination should be implemented for large task lists

### NFR-002: Security
- All API endpoints must require authentication
- User data must be properly isolated
- JWT tokens must be properly validated and have reasonable expiration
- Input must be validated and sanitized on both frontend and backend
- Passwords must be hashed with bcrypt with proper salt
- SQL injection must be prevented through ORM usage
- Cross-site scripting (XSS) must be prevented with proper output encoding

### NFR-003: Usability
- The web interface should be intuitive and responsive
- Error messages should be clear and helpful
- The application should provide loading states for operations
- The interface should work on desktop and mobile devices
- Input fields should properly display typed text without flickering
- Forms should provide immediate validation feedback

### NFR-004: Reliability
- The application should handle network errors gracefully
- The application should provide appropriate error messages
- Database operations should be atomic where appropriate
- The application should maintain data consistency
- Failed operations should not corrupt existing data

### NFR-005: Compatibility
- The application should work with modern browsers (Chrome, Firefox, Safari, Edge)
- The application should be compatible with both light and dark mode UI
- The application should maintain data integrity when using PostgreSQL (migration ready)

## Technical Requirements

### Technology Stack
- Frontend: Next.js 16+ with App Router, TypeScript, Tailwind CSS
- Backend: Python FastAPI with async support
- ORM: SQLModel with proper relationship handling
- Database: SQLite (local development) with PostgreSQL compatibility
- Authentication: JWT-based with bcrypt password hashing
- Claude Code for implementation following Spec-Kit Plus

### Project Structure
```
Phase_II/
├── specs/                        # Specification files
│   ├── phase2-spec.md            # Phase II specification
│   └── other spec files...
├── backend/                      # FastAPI backend
│   ├── main.py                   # FastAPI app entry point
│   ├── models.py                 # SQLModel database models
│   ├── database.py               # Database connection
│   ├── auth.py                   # Authentication utilities (JWT-based)
│   ├── routes/
│   │   ├── auth.py               # Authentication endpoints
│   │   └── tasks.py              # Task endpoints
│   ├── services/
│   │   ├── auth_service.py       # Authentication business logic
│   │   └── task_service.py       # Task business logic
│   ├── .env                      # Environment variables
│   └── requirements.txt          # Python dependencies
├── frontend/                     # Next.js frontend
│   ├── app/                      # App Router pages
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── login/
│   │   ├── signup/
│   │   └── dashboard/
│   ├── components/               # Reusable components
│   │   ├── AddTaskForm.tsx
│   │   ├── TaskCard.tsx
│   │   └── TaskList.tsx
│   ├── lib/                      # Utilities and API client
│   │   └── api.ts
│   ├── types/                    # TypeScript definitions
│   │   └── index.ts
│   ├── public/                   # Static assets
│   ├── .env.local                # Environment variables
│   ├── package.json              # Node.js dependencies
│   ├── next.config.mjs           # Next.js configuration
│   ├── tsconfig.json             # TypeScript configuration
│   └── tailwind.config.ts        # Tailwind CSS configuration
├── SUMMARY.md                    # Implementation summary
├── TESTING_GUIDE.md              # Testing instructions
├── sp.constitution               # Project constitution
└── README.md                     # Project documentation
```

### Database Schema
- **users** table:
  - id: integer (primary key, auto-increment)
  - email: string (unique, not null)
  - name: string (nullable)
  - password_hash: string (not null)
  - created_at: datetime (default now)
  - updated_at: datetime (default now, auto-update)

- **tasks** table:
  - id: integer (primary key, auto-increment)
  - user_id: integer (foreign key → users.id, not null)
  - title: string (not null, 1-200 characters)
  - description: text (nullable, max 1000 characters)
  - completed: boolean (default false)
  - created_at: datetime (default now)
  - updated_at: datetime (default now, auto-update)

### API Endpoints
- **Authentication API**
  - POST /auth/register - Register new user with validation
  - POST /auth/login - Authenticate user and return JWT token
  - GET /auth/me - Get current user info from token

- **Tasks API**
  - GET /api/{user_id}/tasks - List all tasks for a user
  - POST /api/{user_id}/tasks - Create a new task for a user
  - GET /api/{user_id}/tasks/{task_id} - Get specific task for a user
  - PUT /api/{user_id}/tasks/{task_id} - Update a specific task for a user
  - DELETE /api/{user_id}/tasks/{task_id} - Delete a specific task for a user
  - PATCH /api/{user_id}/tasks/{task_id}/complete - Toggle completion status

### Frontend Pages
- `/` - Landing page with introduction and login/signup options
- `/login` - User login form with email/password fields and validation
- `/signup` - User registration form with email, name, password fields and validation
- `/dashboard` - Main task management interface with task list and add form

## Acceptance Criteria

### AC-001: Authentication Implementation
- [x] Users can create accounts via signup form with 6-72 character password validation
- [x] Users can log in with existing credentials
- [x] JWT tokens are properly issued and validated
- [x] API requests include Authorization header with Bearer token
- [x] Users are properly isolated (can't see others' tasks)

### AC-002: Task Creation API
- [x] POST /api/{user_id}/tasks endpoint works correctly
- [x] Task creation validates input properly
- [x] Created tasks are stored in database
- [x] Response includes complete task object
- [x] Authentication is required and validated

### AC-003: Task Listing API
- [x] GET /api/{user_id}/tasks endpoint works correctly
- [x] Only returns tasks for authenticated user
- [x] Supports query parameters for filtering and sorting
- [x] Returns properly formatted task objects
- [x] Authentication is required and validated

### AC-004: Task Retrieval API
- [x] GET /api/{user_id}/tasks/{task_id} endpoint works correctly
- [x] Returns single task object with all details
- [x] Returns 404 for non-existent tasks
- [x] Validates task ownership
- [x] Authentication is required and validated

### AC-005: Task Update API
- [x] PUT /api/{user_id}/tasks/{task_id} endpoint works correctly
- [x] Updates task in database
- [x] Validates input data
- [x] Returns updated task object
- [x] Authentication is required and validated

### AC-006: Task Deletion API
- [x] DELETE /api/{user_id}/tasks/{task_id} endpoint works correctly
- [x] Removes task from database
- [x] Returns success response
- [x] Returns 404 for non-existent tasks
- [x] Authentication is required and validated

### AC-007: Task Completion API
- [x] PATCH /api/{user_id}/tasks/{task_id}/complete endpoint works correctly
- [x] Toggles completion status in database
- [x] Returns updated task object
- [x] Returns 404 for non-existent tasks
- [x] Authentication is required and validated

### AC-008: Frontend Interface
- [x] Responsive design works on desktop and mobile
- [x] All 5 Basic Level operations available via UI
- [x] Proper feedback for all operations
- [x] Authentication state is maintained
- [x] Tasks are displayed with proper status indicators
- [x] Input fields properly display text as user types
- [x] Data persists across page refreshes

### AC-009: Authentication API
- [x] POST /auth/register endpoint works with password validation (6-72 chars)
- [x] POST /auth/login endpoint works with credential validation
- [x] GET /auth/me endpoint works with token validation
- [x] JWT tokens properly stored and retrieved from localStorage
- [x] Bcrypt password hashing with proper security

## Error Handling
- API endpoints return appropriate HTTP status codes (200, 400, 401, 403, 404, 500)
- Frontend displays user-friendly error messages without exposing internal details
- Validation errors are properly handled with clear feedback
- Authentication failures are handled gracefully with appropriate redirects
- Database errors are caught and handled appropriately with proper logging
- Input fields provide real-time validation feedback without disrupting user experience