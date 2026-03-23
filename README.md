# Collaborative Task Board

A production-ready full-stack task management application with real-time synchronization and conflict handling.

## ✨ Features

- ✅ Create, update, and delete tasks
- ✅ Assign tasks to users
- ✅ Real-time polling-based synchronization (3-second interval)
- ✅ Optimistic UI updates with conflict resolution
- ✅ Version-based concurrency control
- ✅ Responsive Kanban board design
- ✅ PostgreSQL database with Neon
- ✅ Production-ready deployment

## 🛠 Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | React 18, TypeScript, Vite, Axios |
| Backend | Starlette, Uvicorn, Gunicorn |
| Database | PostgreSQL (Neon) |
| Deployment | Render (backend), Vercel (frontend) |

## 🚀 Quick Start

### Prerequisites

- Node.js 16+ (frontend)
- Python 3.11+ (backend)
- PostgreSQL database (or Neon account)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your DATABASE_URL
python main.py
```

Backend runs on `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Frontend runs on `http://localhost:5173`

## 🏗 Architecture & System Design

### System Architecture

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

### Data Flow Diagrams

#### Create Task
```
User Input → Frontend → POST /tasks → Backend → Database → Response → UI Update
```

#### Update Task (with Conflict Resolution)
```
User Edit → Frontend (optimistic update) → PUT /tasks/{id} → Backend
  ↓
Check version match
  ├─ Match: Update DB, increment version, return 200
  └─ Mismatch: Return 409 with latest data → Frontend reconciles
```

#### Polling Sync
```
Every 3 seconds:
Frontend → GET /tasks → Backend → Database → Return all tasks → Merge with local state
```

## 🔄 Conflict Handling Approach

The application uses **Optimistic Concurrency Control (OCC)** to handle concurrent updates:

### How It Works

1. **Version Tracking**: Each task has a `version` number that increments with every update
2. **Optimistic Updates**: UI updates immediately when user makes changes (before server confirmation)
3. **Version Validation**: When sending updates to server, client includes the current version number
4. **Server Validation**:
   - If version matches: Update succeeds, version increments, return 200 OK
   - If version mismatch: Conflict detected, return 409 Conflict with latest task data
5. **Conflict Resolution**: When conflict occurs, frontend receives latest data and automatically reconciles

### Example Scenario

```
Time 1: User A fetches task (version: 1)
Time 2: User B fetches same task (version: 1)
Time 3: User A updates task → Server accepts (version: 2)
Time 4: User B tries to update with version: 1 → Server rejects with 409
Time 5: User B receives latest task (version: 2) and can retry update
```

### Benefits

- **No Lost Updates**: Version mismatch prevents overwriting concurrent changes
- **Optimistic UX**: UI feels responsive with immediate updates
- **Automatic Reconciliation**: Conflicts are detected and resolved automatically
- **Scalable**: Works well with polling-based sync without requiring WebSockets

## 📁 Project Structure

```
.
├── backend/
│   ├── main.py              # Starlette app & routes
│   ├── database.py          # PostgreSQL connection
│   ├── models.py            # Data models
│   ├── schemas.py           # Request/response schemas
│   ├── requirements.txt      # Python dependencies
│   ├── Procfile             # Render deployment config
│   ├── runtime.txt          # Python version
│   ├── .python-version      # Python version for Render
│   └── .env.example         # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # Main React component
│   │   ├── api.ts           # API client with polling
│   │   ├── App.css          # Styles
│   │   └── main.tsx         # Entry point
│   ├── package.json         # Node dependencies
│   ├── vite.config.ts       # Vite configuration
│   ├── tsconfig.json        # TypeScript config
│   └── .env.example         # Environment variables template
└── README.md                # This file
```

## 🌐 API Endpoints

### Users
- `POST /users` - Create a new user
- `GET /users` - Get all users

### Tasks
- `POST /tasks` - Create a new task
- `GET /tasks` - Get all tasks (used for polling)
- `PUT /tasks/{task_id}` - Update a task (with version check)
- `DELETE /tasks/{task_id}` - Delete a task

### Health
- `GET /health` - Service health check

## 🚢 Deployment

### Backend (Render)

1. Go to https://render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `collaborative-task-board-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 2 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT`
   - **Root Directory**: `backend`
5. Add environment variable:
   - **Key**: `DATABASE_URL`
   - **Value**: Your Neon PostgreSQL connection string
6. Deploy

### Frontend (Vercel)

1. Update `frontend/.env.production` with your backend URL
2. Go to https://vercel.com
3. Import your GitHub repository
4. Configure:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Deploy

## 🤝 Contributing

Contributions are welcome! Feel free to fork, make changes, and submit pull requests.

## 📝 License

MIT License - feel free to use this project for learning and development.
