# Phase II Specification Clarifications

## Clarified Requirements

### 1. API Endpoint Correction
**Issue:** The documentation shows `/api/{user_id}tasks/{id}` but this appears to be a typo.
**Clarification:** All API endpoints should follow the format `/api/{user_id}/tasks/{id}` with proper path separation.
- GET `/api/{user_id}/tasks` - List all tasks for user
- POST `/api/{user_id}/tasks` - Create a new task
- GET `/api/{user_id}/tasks/{id}` - Get task details
- PUT `/api/{user_id}/tasks/{id}` - Update a task
- DELETE `/api/{user_id}/tasks/{id}` - Delete a task
- PATCH `/api/{user_id}/tasks/{id}/complete` - Toggle completion

### 2. JWT Token Configuration
**Issue:** Need to clarify JWT token configuration between Better Auth and FastAPI.
**Clarification:**
- Better Auth must be configured with JWT plugin to issue tokens
- Both frontend and backend must use the same BETTER_AUTH_SECRET
- JWT tokens must include user ID for authorization
- Backend middleware must verify JWT and extract user information
- Token should have appropriate expiration (e.g., 7 days)

### 3. User Isolation Mechanism
**Issue:** Clarify how user ID in URL path matches authenticated user.
**Clarification:**
- All API requests must include JWT token in Authorization header
- Backend middleware validates JWT and extracts user ID
- The user_id in the URL path must match the authenticated user's ID
- Return 403 Forbidden if user tries to access another user's data
- All database queries must be filtered by authenticated user's ID

### 4. Database Schema Details
**Issue:** Clarify the relationship between Better Auth users and custom tasks.
**Clarification:**
- Users table is managed by Better Auth with id as string primary key
- Tasks table has user_id as string foreign key referencing users.id
- Tasks.user_id must match the authenticated user's ID for all operations
- Proper indexing on tasks.user_id for efficient queries

### 5. Frontend-Backend Communication
**Issue:** Clarify how the Next.js frontend will communicate with FastAPI backend.
**Clarification:**
- Frontend API calls must include Authorization: Bearer <token> header
- Frontend must handle JWT token storage and retrieval
- Frontend must redirect to login when authentication fails
- Proper error handling for both authentication and API errors