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

## 📚 Documentation

- [DEPLOY.md](./DEPLOY.md) - Production deployment guide
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System design and architecture
- [CONTRIBUTING.md](./CONTRIBUTING.md) - Contributing guidelines

## 🔄 How It Works

### Polling Sync
Every 3 seconds, the frontend fetches the latest tasks from the backend and merges changes with local state.

### Conflict Resolution
Uses **Optimistic Concurrency Control (OCC)**:
- Each task has a version number
- Updates include the current version
- Server rejects mismatched versions with 409 Conflict
- Client receives latest data and retries

### Optimistic Updates
UI updates immediately on user action, then syncs with server. If conflict occurs, UI reconciles automatically.

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
├── DEPLOY.md                # Deployment instructions
├── ARCHITECTURE.md          # System architecture
├── CONTRIBUTING.md          # Contributing guide
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
1. Push code to GitHub
2. Connect repository to Render
3. Set root directory to `backend`
4. Add `DATABASE_URL` environment variable
5. Deploy

### Frontend (Vercel)
1. Push code to GitHub
2. Import repository to Vercel
3. Set root directory to `frontend`
4. Deploy

See [DEPLOY.md](./DEPLOY.md) for detailed instructions.

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## 📝 License

MIT License - feel free to use this project for learning and development.
