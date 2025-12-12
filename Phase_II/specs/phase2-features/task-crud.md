# Feature: Task CRUD Operations for Phase II

## User Stories
- As a logged-in user, I can create a new task via the web interface
- As a logged-in user, I can view all my tasks in the web interface
- As a logged-in user, I can update a task's details via the web interface
- As a logged-in user, I can delete a task from the web interface
- As a logged-in user, I can mark a task complete/incomplete via the web interface

## Acceptance Criteria

### Create Task (API)
- Endpoint: POST /api/{user_id}/tasks
- Request body: {title: string (1-200 chars), description: string (optional, max 1000 chars)}
- Response: Created task object with id, title, description, completed, timestamps
- Authentication: JWT token required in Authorization header
- Validation: Title length, user ownership verification
- Error responses: 400 for validation errors, 401 for auth failure, 404 for invalid user

### View Tasks (API)
- Endpoint: GET /api/{user_id}/tasks
- Query params: status (all|pending|completed), sort (created|title|due_date)
- Response: Array of task objects for the authenticated user
- Authentication: JWT token required in Authorization header
- Validation: User ownership verification
- Error responses: 401 for auth failure, 404 for invalid user

### Get Task (API)
- Endpoint: GET /api/{user_id}/tasks/{id}
- Response: Single task object with all details
- Authentication: JWT token required in Authorization header
- Validation: Task belongs to authenticated user
- Error responses: 401 for auth failure, 404 for non-existent task or user mismatch

### Update Task (API)
- Endpoint: PUT /api/{user_id}/tasks/{id}
- Request body: {title: string (optional), description: string (optional)}
- Response: Updated task object
- Authentication: JWT token required in Authorization header
- Validation: Task belongs to authenticated user, input validation
- Error responses: 400 for validation errors, 401 for auth failure, 404 for non-existent task

### Delete Task (API)
- Endpoint: DELETE /api/{user_id}/tasks/{id}
- Response: Success confirmation
- Authentication: JWT token required in Authorization header
- Validation: Task belongs to authenticated user
- Error responses: 401 for auth failure, 404 for non-existent task

### Mark Complete/Incomplete (API)
- Endpoint: PATCH /api/{user_id}/tasks/{id}/complete
- Response: Updated task object
- Authentication: JWT token required in Authorization header
- Validation: Task belongs to authenticated user
- Error responses: 401 for auth failure, 404 for non-existent task

### Frontend Implementation
- Add task form with title and description fields
- Task list displaying all user tasks with status indicators
- Edit task functionality with form pre-filled with current values
- Delete confirmation dialog
- Complete/incomplete toggle buttons
- Proper loading states and error handling
- Responsive design for different screen sizes