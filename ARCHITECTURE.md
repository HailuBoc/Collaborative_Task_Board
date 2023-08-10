# Architecture Overview

## System Design

The Collaborative Task Board is a full-stack web application with real-time synchronization capabilities.

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React + TypeScript)            │
│  - Task management UI                                        │
│  - User assignment interface                                 │
│  - Polling-based sync (3s interval)                          │
│  - Optimistic UI updates                                     │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/REST API
                     │
┌────────────────────▼────────────────────────────────────────┐
│              Backend (Starlette + Uvicorn)                   │
│  - RESTful API endpoints                                     │
│  - Conflict resolution (version-based OCC)                   │
│  - CORS middleware                                           │
│  - Database connection pooling                               │
└────────────────────┬────────────────────────────────────────┘
                     │ SQL Queries
                     │
┌────────────────────▼────────────────────────────────────────┐
│            Database (PostgreSQL via Neon)                    │
│  - Users table                                               │
│  - Tasks table with versioning                               │
│  - Foreign key relationships                                 │
└─────────────────────────────────────────────────────────────┘
```

## Key Components

### Frontend (`frontend/src/`)

- **App.tsx**: Main React component with task management logic
- **api.ts**: Axios-based API client with polling mechanism
- **App.css**: Styling for the UI

### Backend (`backend/`)

- **main.py**: Starlette application with route definitions
- **database.py**: PostgreSQL connection management
- **models.py**: Data models (User, Task)
- **schemas.py**: Request/response validation schemas

## Data Flow

### Create Task
```
User Input → Frontend → POST /tasks → Backend → Database → Response → UI Update
```

### Update Task (with Conflict Resolution)
```
User Edit → Frontend (optimistic update) → PUT /tasks/{id} → Backend
  ↓
Check version match
  ├─ Match: Update DB, increment version, return 200
  └─ Mismatch: Return 409 with latest data → Frontend reconciles
```

### Polling Sync
```
Every 3 seconds:
Frontend → GET /tasks → Backend → Database → Return all tasks → Merge with local state
```

## Conflict Resolution Strategy

Uses **Optimistic Concurrency Control (OCC)**:

1. Each task has a `version` number
2. Client sends current version with update
3. Server compares versions:
   - **Match**: Update succeeds, version increments
   - **Mismatch**: Return 409 Conflict with latest task data
4. Client receives conflict, merges changes, retries

This prevents lost updates in concurrent scenarios.

## Deployment Architecture

### Backend (Render)
- Python 3.11.0
- Gunicorn + Uvicorn workers
- PostgreSQL connection via Neon
- Environment variables for secrets

### Frontend (Vercel)
- Vite build optimization
- Static hosting
- Environment-based API URL configuration

## API Endpoints

### Users
- `POST /users` - Create user
- `GET /users` - List all users

### Tasks
- `POST /tasks` - Create task
- `GET /tasks` - List all tasks (polling)
- `PUT /tasks/{id}` - Update task (with version check)
- `DELETE /tasks/{id}` - Delete task

### Health
- `GET /health` - Service health check

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, TypeScript, Vite, Axios |
| Backend | Starlette, Uvicorn, Gunicorn |
| Database | PostgreSQL (Neon) |
| Deployment | Render (backend), Vercel (frontend) |

## Performance Considerations

- **Polling Interval**: 3 seconds (configurable)
- **Worker Processes**: 2-4 Gunicorn workers
- **Connection Pooling**: Handled by psycopg2
- **CORS**: Configured for production domains
- **Optimistic Updates**: Reduces perceived latency

## Security

- Environment variables for sensitive data
- CORS middleware for cross-origin requests
- SSL/TLS for database connections
- Input validation on all endpoints
- Version-based conflict prevention
