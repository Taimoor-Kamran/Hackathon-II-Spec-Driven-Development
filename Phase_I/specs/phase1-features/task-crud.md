# Feature: Task CRUD Operations for Phase I

## User Stories
- As a user, I can create a new task in the console app
- As a user, I can view all my tasks in the console
- As a user, I can update a task's details in the console
- As a user, I can delete a task from the console
- As a user, I can mark a task complete/incomplete in the console

## Acceptance Criteria

### Create Task
- Title is required (1-200 characters)
- Description is optional (max 1000 characters)
- Task gets a unique ID and timestamps automatically
- Task is stored in-memory
- Confirmation message is shown

### View Tasks
- All tasks are displayed with ID, title, status, and timestamps
- Completed tasks are visually distinct from pending tasks
- Empty list is handled gracefully
- Tasks are displayed in a readable format

### Update Task
- User can update title and/or description by ID
- System validates that task exists before updating
- Updated timestamp is automatically set
- Confirmation message is shown

### Delete Task
- User can delete a task by ID
- System validates that task exists before deletion
- Task is removed from memory
- Confirmation message is shown

### Mark Complete/Incomplete
- User can toggle completion status by ID
- System validates that task exists before updating
- Updated timestamp is automatically set
- Confirmation message is shown