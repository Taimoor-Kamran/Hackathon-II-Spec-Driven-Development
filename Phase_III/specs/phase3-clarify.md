# Phase III: Advanced Todo Web Application - Clarification

## Overview
This document clarifies ambiguities and provides detailed explanations for the Phase III Advanced Todo Web Application specification. It addresses potential questions and decisions that arose during the specification review process.

## Clarified Requirements

### 1. AI-Powered Task Suggestions
**Original Ambiguity:** What exactly constitutes "AI-powered" suggestions?
**Clarification:** For Phase III, AI-powered suggestions will be implemented using rule-based algorithms that analyze:
- Historical task completion patterns
- Task titles and descriptions
- Time-based patterns (tasks typically created on certain days/dates)
- Category and tag usage patterns
- Frequency of similar tasks

The system will not use external AI services or machine learning models but will implement intelligent rule-based recommendations based on user behavior data stored in the database.

### 2. Real-Time Collaboration
**Original Ambiguity:** What level of collaboration is required?
**Clarification:** Real-time collaboration will include:
- Real-time task updates (when a collaborator updates a task, others see changes immediately)
- Real-time status changes (when a collaborator marks a task as complete/incomplete)
- Conflict resolution when multiple users edit the same task simultaneously
- Collaborator presence indicators
- Basic permission system (read-only vs. edit permissions)

For Phase III, collaboration will be implemented through a shared task model where users can be added to specific tasks, rather than full team workspaces.

### 3. Advanced Search and Filtering
**Original Ambiguity:** What search capabilities are expected?
**Clarification:** Advanced search and filtering will include:
- Full-text search across task titles and descriptions
- Filter by completion status (all, pending, completed)
- Filter by category
- Filter by tags (multiple tags possible)
- Filter by due date ranges (overdue, today, this week, this month, custom range)
- Filter by priority (low, medium, high)
- Sort by: creation date, due date, priority, title
- Combined filters (AND logic for multiple filters)

### 4. Task Categories vs Tags
**Original Ambiguity:** What's the difference between categories and tags?
**Clarification:**
- Categories: Hierarchical, single-category assignment per task, used for major organizational grouping (e.g., Work, Personal, Shopping)
- Tags: Multiple tags per task, non-hierarchical, used for detailed classification (e.g., urgent, @work, @home, project-x)

### 5. Due Dates and Reminders
**Original Ambiguity:** How should reminders work?
**Clarification:**
- Due dates: Optional datetime field on tasks
- Reminders: Configurable time before due date to send notification (options: at due time, 1 hour before, 1 day before, custom time)
- Reminder delivery: Real-time via WebSocket connection
- Reminder status: Track whether reminder was sent, acknowledged, or dismissed
- Recurring reminders: For recurring tasks, reminders should also follow the recurrence pattern

### 6. Recurring Tasks
**Original Ambiguity:** What recurrence patterns are supported?
**Clarification:** Recurring tasks will support:
- Daily: Every N days
- Weekly: Every N weeks on specific days of the week
- Monthly: Every N months on specific day of month or relative to occurrence (e.g., "first Monday of month")
- Yearly: Every N years on specific date
- Custom: Combination of patterns with end date or occurrence limit
- Exceptions: Ability to skip specific instances of recurring tasks

### 7. Performance Requirements
**Original Ambiguity:** What are the specific performance expectations?
**Clarification:**
- API endpoints should respond within 1 second for datasets up to 10,000 tasks
- Search operations should return results within 500ms for up to 10,000 tasks
- WebSocket connections should maintain under 100ms latency
- Frontend should handle up to 1,000 tasks in memory without performance degradation
- Database queries should use proper indexing to meet these requirements

### 8. Security and User Isolation
**Original Ambiguity:** How does collaboration interact with user isolation?
**Clarification:**
- Users still maintain data isolation by default
- Collaboration is opt-in: users can share specific tasks with other users
- When sharing a task, the owner can set permissions (view-only or edit)
- Users can only see tasks they own or that have been shared with them
- User A cannot access User B's tasks unless explicitly shared
- Collaboration does not break the fundamental user isolation principle

### 9. Frontend Architecture
**Original Ambiguity:** How should the frontend handle real-time updates?
**Clarification:**
- Use React Context or Zustand for state management
- WebSocket connection established per user session
- Real-time updates should update local state immediately
- Conflict resolution: last-write-wins with optimistic updates
- Connection status indicators for real-time features
- Graceful degradation when WebSocket is unavailable

### 10. Database Design
**Original Ambiguity:** How should recurring tasks be stored?
**Clarification:**
- Original recurring task template stored in tasks table with recurrence metadata
- Generated instances stored as separate task entries with reference to template
- Template changes should optionally update all future instances
- Completed instances remain as historical records
- Recurrence rules stored in separate recurring_tasks table
- Each generated instance has its own due dates, reminders, and status

## Technical Decisions

### 1. WebSocket Implementation
- Use FastAPI's WebSocket support for real-time features
- Implement connection management with user authentication
- Use JSON messages for communication protocol
- Implement automatic reconnection logic in frontend

### 2. Search Implementation
- Use SQL full-text search capabilities where available
- Implement efficient indexing on searchable fields
- Use pagination for large result sets
- Consider search result ranking by relevance

### 3. Task Scheduling for Reminders
- Use a background task system (e.g., Celery with Redis)
- Or implement a simple scheduler within the application
- Store reminder tasks in database with scheduled execution time
- Send reminders via WebSocket when due

### 4. Recurring Task Generation
- Generate future task instances on-demand or periodically
- Use cron-like scheduling for recurring task creation
- Allow users to generate instances in advance (e.g., next 30 days)
- Clean up old instances that are no longer needed

## Implementation Order Considerations

### Phase 3A: Foundation Features
1. Enhanced database models (categories, tags, due dates, reminders)
2. Basic API endpoints for new features
3. Frontend components for new features
4. Integration with existing Phase I & II functionality

### Phase 3B: Advanced Features
1. Real-time collaboration with WebSockets
2. Advanced search and filtering
3. Recurring task functionality
4. AI-powered suggestions

### Phase 3C: Polish and Optimization
1. Performance optimization
2. Error handling and edge cases
3. Testing and quality assurance
4. Documentation updates

## Dependencies and Constraints

### 1. Database Constraints
- Maintain backward compatibility with existing data from Phase II
- Use proper foreign key relationships
- Implement proper indexing for performance
- Handle database migrations safely

### 2. Frontend Constraints
- Maintain responsive design across all new features
- Ensure accessibility standards
- Keep bundle sizes reasonable with code splitting
- Maintain good UX with loading states and error handling

### 3. Security Constraints
- All new endpoints must validate JWT tokens
- User data isolation must be maintained
- Input validation and sanitization required
- No direct user-to-user access without explicit sharing

## Questions for Further Clarification

1. Should AI suggestions be generated in real-time or pre-computed periodically?
2. What is the expected maximum number of concurrent WebSocket connections?
3. Should recurring tasks support complex patterns like "last weekday of month"?
4. How should the system handle time zones for due dates and reminders?
5. Should there be different levels of collaboration (task-level vs. project-level sharing)?
6. What happens to recurring tasks when the original template is deleted?
7. Should there be a limit on the number of tags per task or categories per user?
8. How should the system handle conflicts during real-time collaboration?

## Assumptions

1. The application will be used primarily by individual users with occasional collaboration
2. Users will have at most hundreds of tasks, not thousands (for performance)
3. Real-time collaboration will involve small groups (2-5 people typically)
4. Users have reliable internet connections for WebSocket features
5. The application is deployed in a single time zone context initially
6. External AI services are not available or cost-prohibitive
7. Users want simplicity over feature complexity
8. Data privacy and isolation are paramount concerns