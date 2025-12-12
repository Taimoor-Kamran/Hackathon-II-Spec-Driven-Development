# Phase II Testing Guide

## How to Test Phase II Todo Full-Stack Web Application

### Prerequisites
- Python 3.8+
- Node.js 18+ for frontend
- npm package manager

### Backend Setup and Testing

1. **Navigate to backend directory:**
   ```bash
   cd /home/taimoor/Hackathon_II/Phase_II/backend
   ```

2. **Set up environment variables:**
   Create a `.env` file in the backend directory with:
   ```
   DATABASE_URL=sqlite:///./todo_app.db
   JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the backend:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```
   The backend will be available at `http://localhost:8000` or `http://localhost:8001` if port 8000 is in use

5. **Test API endpoints manually:**
   - Visit `http://localhost:8000/docs` or `http://localhost:8001/docs` for interactive API documentation
   - Test the `/health` endpoint at `http://localhost:8000/health` or `http://localhost:8001/health`
   - Test the root endpoint at `http://localhost:8000/` or `http://localhost:8001/`

### Frontend Setup and Testing

1. **Navigate to frontend directory:**
   ```bash
   cd /home/taimoor/Hackathon_II/Phase_II/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables:**
   Create a `.env.local` file in the frontend directory with:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

   The `NEXT_PUBLIC_API_URL` environment variable tells the frontend where to find the backend API. If the backend is running on a different port (e.g., 8001 if port 8000 is in use), update this variable accordingly.

4. **Run the frontend:**
   ```bash
   npm run dev
   # OR if you encounter Turbopack errors:
   npx next dev -p 3001
   ```
   The frontend will be available at `http://localhost:3000` or `http://localhost:3001`

### Complete Integration Testing

1. **Start both backend and frontend servers**
2. **Open browser to `http://localhost:3000` or `http://localhost:3001`**
3. **Test the complete user flow:**

   a. **Authentication Flow:**
   - Navigate to `/signup` page
   - Register a new account with valid details (email, name, password 6-72 characters)
   - Navigate to `/login` page
   - Login with your credentials
   - You will be redirected to `/dashboard`

   b. **Dashboard and Task Management:**
   - Verify you can see the "Todo Dashboard" header
   - Test adding a new task using the form (type in title and description)
   - Verify the new task appears in the task list
   - Test marking a task as complete/incomplete using the checkbox
   - Test deleting a task using the delete button
   - Verify tasks persist after page refresh

   c. **User Isolation:**
   - Register a second user account
   - Login with the second account
   - Verify you only see tasks created by this user
   - Verify you cannot access other users' tasks

### Manual API Testing with curl

If you want to test the backend API directly:

1. **Register a new user:**
   ```bash
   curl -X POST http://localhost:8000/auth/register \
     -H "Content-Type: application/json" \
     -d '{"name": "Test User", "email": "test@example.com", "password": "password123"}'
   ```

2. **Login to get JWT token:**
   ```bash
   curl -X POST http://localhost:8000/auth/login \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "email=test@example.com&password=password123"
   ```

3. **Create a task (using the user ID from login response):**
   ```bash
   curl -X POST http://localhost:8000/api/1/tasks \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
     -d '{"title": "Test task", "description": "Test description"}'
   ```

4. **List tasks:**
   ```bash
   curl -X GET http://localhost:8000/api/1/tasks \
     -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
   ```

5. **Update a task (replace {id} with actual task ID):**
   ```bash
   curl -X PUT http://localhost:8000/api/1/tasks/{id} \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
     -d '{"title": "Updated task title", "description": "Updated description"}'
   ```

6. **Toggle task completion:**
   ```bash
   curl -X PATCH http://localhost:8000/api/1/tasks/{id}/complete \
     -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
   ```

7. **Delete a task:**
   ```bash
   curl -X DELETE http://localhost:8000/api/1/tasks/{id} \
     -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
   ```

8. **Test user isolation (try to access another user's tasks):**
   ```bash
   curl -X GET http://localhost:8000/api/2/tasks \
     -H "Authorization: Bearer YOUR_USER_1_JWT_TOKEN_HERE"
   # Should return 403 Forbidden
   ```

### API Endpoints Reference

#### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info

#### Tasks
- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{task_id}` - Update a task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle completion status

### Expected Functionality

- [x] Backend server starts without errors
- [x] Frontend server starts without errors
- [x] User registration works (with 6-72 character password validation)
- [x] User login works with JWT token storage
- [x] Dashboard page displays correctly after login
- [x] Add task form works with proper input field display
- [x] Task list displays tasks for current user
- [x] Task creation persists to database
- [x] Mark task as complete/incomplete works
- [x] Delete task functionality works
- [x] User isolation - users only see their own tasks
- [x] Tasks persist after page refresh
- [x] Input fields properly display typed text
- [x] Proper error handling for authentication
- [x] Logout functionality works

### Troubleshooting

- **If the backend fails to start**, check that your `.env` file has the correct DATABASE_URL
- **If the frontend fails to connect to the backend**, verify NEXT_PUBLIC_API_URL is set correctly
- **If input fields don't show typed text**, check browser console for errors
- **If authentication fails**, ensure you're using correct credentials
- **If tasks don't persist**, verify the SQLite database file is being created
- **If you encounter Turbopack errors**, use `npx next dev -p 3001` instead of `npm run dev`
- **If bcrypt password error occurs**, ensure passwords are 6-72 characters long
- **Check browser console for frontend errors**
- **Check terminal for backend errors**

### Security Features Tested

- [x] JWT token validation
- [x] User ID validation in URLs matches authenticated user
- [x] Password hashing with bcrypt
- [x] User isolation (one user cannot access another's data)
- [x] Input validation and sanitization
- [x] Proper error handling without information disclosure

### Files Included in Phase II
- `backend/` - FastAPI backend with models, routes, services, authentication
- `frontend/` - Next.js frontend with pages, components, API client
- `specs/` - All specification files (constitution, spec, clarify, plan, tasks, adr)
- `TESTING_GUIDE.md` - This file
- `README.md` - Project documentation
- `.gitignore` - Git ignore rules for build artifacts and sensitive files