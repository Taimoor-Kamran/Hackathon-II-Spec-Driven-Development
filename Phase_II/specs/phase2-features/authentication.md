# Feature: Authentication for Phase II

## User Stories
- As a new user, I can create an account
- As a registered user, I can log in to my account
- As a logged-in user, I can log out of my account
- As a logged-in user, my tasks are isolated from other users
- As a user, my credentials are securely stored and transmitted

## Acceptance Criteria

### User Registration
- Endpoint: POST /api/auth/signup (via Better Auth)
- Request body: {email: string, password: string, name: string (optional)}
- Response: User object and JWT token
- Validation: Email format, password strength, unique email
- Error responses: 400 for validation errors, 409 for duplicate email

### User Login
- Endpoint: POST /api/auth/login (via Better Auth)
- Request body: {email: string, password: string}
- Response: User object and JWT token
- Validation: Valid credentials
- Error responses: 400 for validation errors, 401 for invalid credentials

### User Logout
- Endpoint: POST /api/auth/logout (via Better Auth)
- Request: JWT token in Authorization header
- Response: Success confirmation
- Invalidates current session
- Error responses: 401 for invalid token

### JWT Token Configuration
- Better Auth must be configured to issue JWT tokens
- Token includes user ID, email, and other relevant user information
- Token has appropriate expiration time (e.g., 7 days)
- Shared secret key (BETTER_AUTH_SECRET) used by both frontend and backend

### API Authentication Middleware
- All task API endpoints require valid JWT token in Authorization: Bearer <token> header
- Middleware extracts and validates JWT token
- Middleware identifies authenticated user from token
- Requests without valid token receive 401 Unauthorized response
- Requests with valid token but wrong user_id receive 403 Forbidden response

### Frontend Authentication Integration
- Frontend uses Better Auth for login/signup UI
- JWT token stored securely in browser (using Better Auth's mechanisms)
- JWT token automatically attached to all API requests
- Authentication state managed properly (login/logout)
- Redirect to login page when not authenticated
- Proper error handling for authentication failures

### User Isolation
- Each API endpoint filters results by authenticated user's ID
- Users can only access/modify their own tasks
- User ID in URL path must match authenticated user's ID
- Backend verifies user ownership for all operations
- Appropriate error responses when user tries to access other users' data

### Security Requirements
- Passwords stored securely (handled by Better Auth)
- JWT tokens signed with strong algorithm (RS256 recommended)
- Secure transmission over HTTPS in production
- Token refresh mechanism if needed
- Proper session management