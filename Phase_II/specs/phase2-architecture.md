# Phase II Architecture: Full-Stack Web Application

## System Overview
Phase II implements a full-stack web application with a Next.js frontend, FastAPI backend, and Neon PostgreSQL database. The architecture follows a client-server model with JWT-based authentication for secure user isolation.

## Architecture Layers

### 1. Presentation Layer (Frontend)
- **Next.js 16+ App Router**: Handles routing and page rendering
- **React Components**: Reusable UI elements for task management
- **API Client**: HTTP client for communicating with backend API
- **State Management**: Client-side state for UI interactions
- **Authentication Context**: Manages login state and JWT tokens

### 2. API Layer (Backend)
- **FastAPI Application**: ASGI application server
- **Route Handlers**: REST API endpoints for task operations
- **Authentication Middleware**: JWT token validation
- **Request/Response Models**: Pydantic models for data validation
- **Error Handlers**: Proper HTTP error responses

### 3. Business Logic Layer (Backend)
- **Service Classes**: Encapsulates business logic for task operations
- **Validation Logic**: Input validation and business rule enforcement
- **Authentication Services**: User authentication and authorization
- **Error Handling**: Business-level error management

### 4. Data Layer (Backend)
- **SQLModel Models**: Database schema definitions
- **Database Services**: CRUD operations using SQLModel/SQLAlchemy
- **Connection Pooling**: Efficient database connection management
- **Transaction Management**: Ensures data consistency

### 5. Authentication Layer
- **Better Auth**: Handles user registration/login/logout
- **JWT Token Generation**: Creates signed tokens for API authentication
- **Token Validation**: Verifies tokens and extracts user information
- **Session Management**: Maintains user sessions

## Component Structure

```
backend/
├── main.py              # FastAPI app entry point
├── models.py            # SQLModel database models
├── database.py          # Database connection setup
├── auth.py              # Authentication utilities and middleware
├── routes/
│   ├── __init__.py
│   ├── auth.py          # Better Auth integration
│   └── tasks.py         # Task API endpoints
├── services/
│   ├── __init__.py
│   ├── task_service.py  # Business logic for tasks
│   └── auth_service.py  # Business logic for auth
└── requirements.txt

frontend/
├── app/                 # Next.js App Router pages
│   ├── layout.tsx       # Root layout
│   ├── page.tsx         # Landing page
│   ├── login/
│   │   └── page.tsx     # Login page
│   ├── signup/
│   │   └── page.tsx     # Signup page
│   └── dashboard/
│       └── page.tsx     # Main dashboard
├── components/          # Reusable React components
│   ├── TaskList.tsx     # Task list component
│   ├── TaskCard.tsx     # Individual task component
│   ├── AddTaskForm.tsx  # Task creation form
│   └── AuthProvider.tsx # Authentication context
├── lib/
│   ├── api.ts           # API client
│   └── auth.ts          # Authentication utilities
├── styles/              # CSS/SCSS styles
│   └── globals.css      # Global styles
├── types/
│   └── index.ts         # TypeScript type definitions
└── package.json
```

## Database Schema

### Users Table (managed by Better Auth)
- `id`: string (primary key)
- `email`: string (unique, not null)
- `name`: string (nullable)
- `created_at`: timestamp (default now)

### Tasks Table (custom)
- `id`: integer (primary key, auto-increment)
- `user_id`: string (foreign key → users.id, not null)
- `title`: string (not null, 1-200 characters)
- `description`: text (nullable)
- `completed`: boolean (default false)
- `created_at`: timestamp (default now)
- `updated_at`: timestamp (auto-update)

## API Design

### Authentication Flow
1. User registers/logs in via Better Auth
2. Better Auth issues JWT token
3. Frontend stores token and includes in Authorization header
4. Backend middleware validates token
5. User ID extracted from token for authorization

### REST API Endpoints
- `POST /api/auth/[...nextauth]` - Better Auth endpoints
- `GET /api/{user_id}/tasks` - List user's tasks
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion

### Request/Response Format
- Requests: JSON with appropriate validation
- Responses: JSON with consistent structure
- Errors: Standard error format with message and status code
- Authentication: Bearer token in Authorization header

## Security Implementation

### JWT Token Flow
- Better Auth configured with JWT plugin
- Frontend API calls include Authorization: Bearer <token>
- Backend middleware verifies JWT using shared secret
- Token contains user information for authorization
- Requests filtered by authenticated user's ID

### Data Isolation
- All queries filtered by user_id
- Authorization checks in each endpoint
- User ID in URL must match authenticated user
- Proper error responses for unauthorized access

## Deployment Considerations
- Backend API deployed separately from frontend
- CORS configured for frontend domain
- Environment variables for database URL, auth secret, etc.
- SSL/TLS for production security
- Database connection pooling for performance

## Error Handling Strategy
- Frontend: User-friendly error messages and loading states
- Backend: Proper HTTP status codes and error responses
- Network: Retry logic and offline handling
- Validation: Client and server-side validation

## Testing Strategy
- Unit tests for backend services
- Integration tests for API endpoints
- Component tests for frontend components
- End-to-end tests for critical user flows
- Authentication flow testing