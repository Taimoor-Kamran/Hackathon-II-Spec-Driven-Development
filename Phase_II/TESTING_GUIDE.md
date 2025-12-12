# Phase II Testing Guide

## How to Test Phase II Todo Full-Stack Web Application

### Prerequisites
- Python 3.8+ (Python 3.13+ recommended)
- Node.js 18+ for frontend
- PostgreSQL database (or Neon Serverless PostgreSQL)
- UV package manager (install with `pip install uv`)

### Backend Setup and Testing

1. **Navigate to backend directory:**
   ```bash
   cd /home/taimoor/Hackathon_II/Phase_II/backend
   ```

2. **Set up environment variables:**
   Create a `.env` file in the backend directory with:
   ```
   DATABASE_URL=postgresql://user:password@localhost/todo_db
   BETTER_AUTH_SECRET=your-super-secret-jwt-key-change-this-in-production
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # or if using uv: uv pip install -r requirements.txt
   ```

4. **Run the backend:**
   ```bash
   uvicorn main:app --reload
   ```
   The backend will be available at `http://localhost:8000`

5. **Test API endpoints manually:**
   - Visit `http://localhost:8000/docs` for interactive API documentation
   - Test the `/health` endpoint at `http://localhost:8000/health`
   - Test the root endpoint at `http://localhost:8000/`

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

4. **Run the frontend:**
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:3000`

### Complete Integration Testing

1. **Start both backend and frontend servers**
2. **Open browser to `http://localhost:3000`**
3. **Test the complete user flow:**

   a. **Landing Page:**
   - Visit the home page at `http://localhost:3000`
   - Verify you see "Welcome to Todo App" message
   - Verify "Sign in" and "Create account" buttons are present

   b. **Authentication Flow:**
   - Navigate to `/login` page
   - Try to sign in (note: in this implementation, authentication is simulated)
   - Navigate to `/signup` page
   - Try to create an account (simulated)

   c. **Dashboard and Task Management:**
   - Navigate to `/dashboard` page
   - Verify you can see the "Todo Dashboard" header
   - Test adding a new task using the form
   - Verify the new task appears in the task list
   - Test editing an existing task
   - Test marking a task as complete/incomplete
   - Test deleting a task

   d. **API Integration:**
   - In a real implementation, verify all 6 API endpoints work:
     - GET /api/{user_id}/tasks
     - POST /api/{user_id}/tasks
     - GET /api/{user_id}/tasks/{id}
     - PUT /api/{user_id}/tasks/{id}
     - DELETE /api/{user_id}/tasks/{id}
     - PATCH /api/{user_id}/tasks/{id}/complete

### Manual API Testing with curl

If you want to test the backend API directly:

1. **Create a task (simulated user_id "user-123"):**
   ```bash
   curl -X POST http://localhost:8000/api/user-123/tasks \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer fake-jwt-token" \
     -d '{"title": "Test task", "description": "Test description"}'
   ```

2. **List tasks:**
   ```bash
   curl -X GET http://localhost:8000/api/user-123/tasks \
     -H "Authorization: Bearer fake-jwt-token"
   ```

3. **Update a task (replace {id} with actual task ID):**
   ```bash
   curl -X PUT http://localhost:8000/api/user-123/tasks/{id} \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer fake-jwt-token" \
     -d '{"title": "Updated task title", "description": "Updated description"}'
   ```

4. **Toggle task completion:**
   ```bash
   curl -X PATCH http://localhost:8000/api/user-123/tasks/{id}/complete \
     -H "Authorization: Bearer fake-jwt-token"
   ```

5. **Delete a task:**
   ```bash
   curl -X DELETE http://localhost:8000/api/user-123/tasks/{id} \
     -H "Authorization: Bearer fake-jwt-token"
   ```

### Testing User Isolation

In a complete implementation, verify that:
- User A cannot access User B's tasks
- The user_id in the JWT token matches the user_id in the URL
- Requests with mismatched user_ids return 403 Forbidden

### Expected Functionality

- [ ] Backend server starts without errors
- [ ] Frontend server starts without errors
- [ ] Landing page displays correctly
- [ ] Login page displays correctly
- [ ] Signup page displays correctly
- [ ] Dashboard page displays correctly
- [ ] Add task form works
- [ ] Task list displays tasks
- [ ] Edit task functionality works
- [ ] Delete task functionality works
- [ ] Toggle completion works
- [ ] Logout functionality works

### Troubleshooting

- If the backend fails to start, check that your `.env` file has the correct DATABASE_URL
- If the frontend fails to connect to the backend, verify NEXT_PUBLIC_API_URL is set correctly
- If authentication seems to fail, remember that in this implementation it's simulated with localStorage
- Check browser console for frontend errors
- Check terminal for backend errors

### Files Included in Phase II
- `backend/` - FastAPI backend with models, routes, services, authentication
- `frontend/` - Next.js frontend with pages, components, API client
- `specs/` - All specification files (constitution, spec, clarify, plan, tasks, adr)
- `TESTING_GUIDE.md` - This file
- `README.md` - Project documentation