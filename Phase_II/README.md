# Phase II: Todo Full-Stack Web Application

This is Phase II of the Hackathon II project: transforming the Phase I console app into a modern multi-user web application with persistent storage using Next.js, FastAPI, SQLModel, and SQLite for local development.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)
- [Authentication Flow](#authentication-flow)
- [Security](#security)
- [Troubleshooting](#troubleshooting)
- [Development Workflow](#development-workflow)

## Overview

Phase II implements a full-stack web application with:
- Frontend: Next.js 16+ with App Router
- Backend: Python FastAPI
- ORM: SQLModel
- Database: SQLite (for local development) with PostgreSQL option
- Authentication: JWT-based with proper user isolation

## Features

All 5 Basic Level features are implemented:
1. **Add Task** – Create new todo items
2. **Delete Task** – Remove tasks from the list
3. **Update Task** – Modify existing task details
4. **View Task List** – Display all tasks
5. **Mark as Complete** – Toggle task completion status

Additional features:
- User registration and login
- Secure JWT-based authentication
- User isolation (each user sees only their tasks)
- Responsive web interface
- Form validation and error handling
- Password length validation (max 72 characters due to bcrypt limitation)

## Architecture

The application follows a client-server architecture with JWT-based authentication for secure user isolation.

### Backend (FastAPI)
- REST API endpoints with proper authentication
- SQLModel for database operations
- JWT token validation middleware
- User isolation (each user sees only their tasks)
- Password hashing with bcrypt
- Comprehensive error handling

### Frontend (Next.js)
- Responsive web interface with Tailwind CSS
- Task management components
- Authentication state management
- API client with JWT token handling
- Form validation and error boundaries
- Proper React state management

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs with Python
- **SQLModel**: SQL databases in Python, with a focus on type safety
- **Pydantic**: Data validation and settings management
- **python-jose**: JSON Web Token implementation
- **passlib**: Password hashing library with bcrypt
- **uvicorn**: ASGI server for running the application

### Frontend
- **Next.js 16**: React framework with App Router
- **React**: JavaScript library for building user interfaces
- **TypeScript**: Typed superset of JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **JWT-based authentication**: Client-side token management

## Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 18 or higher
- npm or yarn

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd Phase_II/backend
   ```

2. (Optional but recommended) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables (see Environment Variables section)

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd Phase_II/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Running the Application

### Backend
1. Navigate to the backend directory:
   ```bash
   cd Phase_II/backend
   ```

2. Start the backend server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
   The backend will be available at `http://localhost:8000` or `http://localhost:8001` if port 8000 is in use

### Frontend
1. Navigate to the frontend directory:
   ```bash
   cd Phase_II/frontend
   ```

2. Start the frontend server:
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:3000` or `http://localhost:3001` if port 3000 is in use

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login user and get JWT token
- `GET /auth/me` - Get current user info from token

### Tasks
- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task for a user
- `GET /api/{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{task_id}` - Update a specific task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete a specific task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle task completion status

## Environment Variables

### Backend (.env file in Phase_II/backend/)
Create a `.env` file in the backend directory with the following:
```env
DATABASE_URL=sqlite:///./todo_app.db
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
```

### Frontend (.env.local file in Phase_II/frontend/)
Create a `.env.local` file in the frontend directory with the following:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

The `NEXT_PUBLIC_API_URL` environment variable is used by the frontend to connect to the backend API. If the backend is running on a different port (e.g., 8001 if port 8000 is in use), update this variable accordingly.

## Project Structure
```
Phase_II/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── models.py               # SQLModel database models (User, Task)
│   ├── database.py             # Database configuration and connection
│   ├── auth.py                 # Authentication utilities and JWT handling
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables (do not commit)
│   └── routes/
│       ├── tasks.py            # Task-related API routes
│       └── auth.py             # Authentication API routes
│   └── services/
│       ├── task_service.py     # Task business logic
│       └── auth_service.py     # Authentication business logic
├── frontend/
│   ├── app/                    # Next.js App Router pages
│   │   ├── page.tsx            # Home page
│   │   ├── login/page.tsx      # Login page with form validation
│   │   ├── signup/page.tsx     # Signup page with form validation
│   │   └── dashboard/page.tsx  # Dashboard page with task management
│   ├── components/             # Reusable React components
│   │   ├── AddTaskForm.tsx     # Form for adding tasks with state management
│   │   ├── TaskCard.tsx        # Component for displaying individual tasks
│   │   └── TaskList.tsx        # Component for listing multiple tasks
│   ├── lib/                    # Utility functions
│   │   └── api.ts              # API client with JWT token handling
│   ├── types/                  # TypeScript type definitions
│   │   └── index.ts            # Type definitions for Task and related interfaces
│   ├── styles/                 # Global styles
│   │   └── globals.css         # Global CSS styles
│   ├── package.json            # Node.js dependencies
│   ├── next.config.mjs         # Next.js configuration
│   ├── tsconfig.json           # TypeScript configuration
│   └── .env.local              # Environment variables (do not commit)
├── README.md                   # This file
├── SUMMARY.md                  # Project summary
├── TESTING_GUIDE.md            # Testing guide
└── sp.constitution            # Project constitution
```

## Authentication Flow
1. User registers via `/auth/register` with email, name, and password
2. User logs in via `/auth/login` to receive JWT token
3. Token is stored in browser's localStorage
4. Token is sent in Authorization header for protected endpoints
5. Backend verifies token and extracts user ID
6. User ID from token is matched with user ID in URL to ensure proper authorization
7. Each user can only access their own tasks

## Security

- **JWT tokens** for authentication with expiration
- **User ID validation** in URL matches authenticated user
- **Password hashing** with bcrypt (max 72 characters)
- **Input validation** and sanitization on both frontend and backend
- **SQL injection prevention** through ORM (SQLModel)
- **Proper user isolation** - users can only access their own data
- **Form validation** to prevent malicious input

## Troubleshooting

### Common Issues
1. **Port already in use**: Check if another process is using port 8000 or 3000/3001
2. **Database connection errors**: Ensure DATABASE_URL is correctly configured
3. **Authentication errors**: Verify JWT token format and expiration
4. **Frontend build errors**: Clear Next.js cache with `rm -rf .next` in frontend directory
5. **bcrypt password limit**: Passwords must be 6-72 characters due to bcrypt limitation
6. **Turbopack errors**: Use `npx next dev -p 3001` instead of regular dev command

### Development Commands
- **Backend**: `uvicorn main:app --reload --port 8000`
- **Frontend**: `npm run dev` or `npx next dev -p 3001`
- **Install backend deps**: `pip install -r requirements.txt`
- **Install frontend deps**: `npm install`
- **Clear frontend cache**: `rm -rf .next`

### API Testing
You can test the API endpoints using curl:
```bash
# Register a new user
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User", "email":"test@example.com", "password":"password123"}'

# Login to get token
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=test@example.com&password=password123"

# Use the token to access tasks (replace YOUR_TOKEN with actual token)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/1/tasks"
```

## Development Workflow

This project follows the Spec-Driven Development workflow:
1. **Constitution** (/sp.constitution): Define/update project principles
2. **Specify** (/sp.specify): Create features specification with user stories
3. **Clarify** (/sp.clarify): Resolve ambiguities in specifications
4. **Plan** (/sp.plan): Generate technical implementation plan
5. **Tasks** (/sp.tasks): Break down into actionable, testable tasks
6. **Implement** (/sp.implement): Execute tasks using Red-Green-Refactor
7. **Document** (/sp.adr): Record architectural decisions when significant
8. **Record** (/sp.phr): Create prompt History Records for traceability

## Contributing

We welcome contributions to improve this full-stack todo application! Here's how you can contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a pull request

### Development Guidelines
- Follow the existing code style and patterns
- Write clear, descriptive commit messages
- Update documentation when adding new features
- Ensure all tests pass before submitting a pull request

## Deployment

### Backend Deployment
1. Set up your environment with the required dependencies
2. Configure your database connection in the `.env` file
3. Run database migrations if needed
4. Start the FastAPI server

### Frontend Deployment
1. Install frontend dependencies with `npm install`
2. Set environment variables for API endpoints
3. Build the application with `npm run build`
4. Serve the built application

## Project Status

✅ **Phase II Complete**: Full-stack todo application with authentication and task management
- ✅ User registration and login with JWT-based authentication
- ✅ Secure password hashing with bcrypt
- ✅ Task CRUD operations (Create, Read, Update, Delete)
- ✅ Task completion toggling
- ✅ User isolation (users only see their own tasks)
- ✅ Responsive web interface
- ✅ Proper error handling and validation
- ✅ Input field fixes (text now properly displays when typing)
- ✅ Data persistence with SQLite database

## Future Enhancements

Possible future enhancements for Phase III and beyond:
- AI-powered task management
- Real-time collaboration features
- Advanced filtering and search capabilities
- Task categorization and tagging
- Due dates and reminders
- Recurring tasks

## License
This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments
- Built with Next.js, FastAPI, SQLModel, and TypeScript
- Authentication powered by JWT tokens with bcrypt password hashing
- UI designed with Tailwind CSS
- Developed following Spec-Driven Development principles