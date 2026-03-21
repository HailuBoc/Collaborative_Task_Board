# Collaborative Task Board

A full-stack task management system with polling-based sync and optimistic concurrency control.

## Tech Stack

- **Frontend:** React + TypeScript + Vite + Axios
- **Backend:** Python + Starlette + Uvicorn
- **Database:** SQLite

## Features

- Create, update, and delete tasks
- Task statuses: TODO, IN_PROGRESS, DONE
- Assign users to tasks
- Optimistic UI updates with conflict resolution
- Polling-based sync (3-second intervals)
- Version-based concurrency control
- Responsive Kanban board UI

## Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
Backend runs on `http://localhost:8000`

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on `http://localhost:5173`

## Project Structure

```
├── backend/
│   ├── main.py              # Starlette app
│   ├── database.py          # SQLite setup
│   ├── schemas.py           # Data schemas
│   ├── models.py            # Model definitions
│   └── requirements.txt      # Dependencies
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # Main component
│   │   ├── api.ts           # API client
│   │   ├── App.css          # Styling
│   │   └── main.tsx         # Entry point
│   ├── package.json         # NPM config
│   └── vite.config.ts       # Vite config
└── README.md
```

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/users` | Create user |
| GET | `/users` | Get all users |
| POST | `/tasks` | Create task |
| GET | `/tasks` | Get all tasks |
| PUT | `/tasks/{id}` | Update task |
| DELETE | `/tasks/{id}` | Delete task |

## Conflict Resolution

Uses optimistic concurrency control with version tracking:
1. Client sends update with current version
2. Server validates version matches
3. If match: Update and increment version
4. If mismatch: Return 409 Conflict with latest data
5. Frontend reverts UI and shows error message
