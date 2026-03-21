"""
Collaborative Task Board API - Starlette Backend
Core Tech: Starlette (FastAPI's foundation) + SQLite
Implements: Polling-based sync + Optimistic concurrency control
"""

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount
from starlette.middleware.cors import CORSMiddleware
from datetime import datetime
import uuid
import json

from database import get_db


def serialize_task(row):
    """Convert database row to dict"""
    return {
        "id": row["id"],
        "title": row["title"],
        "status": row["status"],
        "assigned_to": row["assigned_to"],
        "updated_at": row["updated_at"],
        "version": row["version"],
    }


def serialize_user(row):
    """Convert database row to dict"""
    return {
        "id": row["id"],
        "name": row["name"],
    }


# ============ User Endpoints ============

async def create_user(request):
    """Create a new user"""
    try:
        data = await request.json()
        if not data.get("name"):
            return JSONResponse({"detail": "Name is required"}, status_code=400)

        user_id = str(uuid.uuid4())
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (id, name) VALUES (?, ?)", (user_id, data["name"]))
            conn.commit()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()
            return JSONResponse(serialize_user(user), status_code=201)
    except Exception as e:
        return JSONResponse({"detail": str(e)}, status_code=400)


async def get_users(request):
    """Get all users"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            return JSONResponse([serialize_user(u) for u in users])
    except Exception as e:
        return JSONResponse({"detail": str(e)}, status_code=400)


# ============ Task Endpoints ============

async def create_task(request):
    """Create a new task"""
    try:
        data = await request.json()
        if not data.get("title"):
            return JSONResponse({"detail": "Title is required"}, status_code=400)

        task_id = str(uuid.uuid4())
        now = datetime.now().isoformat()

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO tasks (id, title, status, assigned_to, updated_at, version)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    task_id,
                    data["title"],
                    data.get("status", "TODO"),
                    data.get("assigned_to"),
                    now,
                    1,
                ),
            )
            conn.commit()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            task = cursor.fetchone()
            return JSONResponse(serialize_task(task), status_code=201)
    except Exception as e:
        return JSONResponse({"detail": str(e)}, status_code=400)


async def get_tasks(request):
    """Get all tasks - used for polling sync"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks")
            tasks = cursor.fetchall()
            return JSONResponse([serialize_task(t) for t in tasks])
    except Exception as e:
        return JSONResponse({"detail": str(e)}, status_code=400)


async def update_task(request):
    """
    Update a task with optimistic concurrency control
    
    Conflict Resolution:
    - Client sends version number with update
    - Server checks if version matches current DB version
    - If mismatch: Return 409 Conflict with latest task data
    - If match: Update task, increment version, return updated task
    """
    try:
        task_id = request.path_params["task_id"]
        data = await request.json()
        
        if "version" not in data:
            return JSONResponse({"detail": "Version is required"}, status_code=400)

        with get_db() as conn:
            cursor = conn.cursor()
            
            # Get current task
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            task = cursor.fetchone()

            if not task:
                return JSONResponse({"detail": "Task not found"}, status_code=404)

            # Optimistic concurrency control - check version
            if task["version"] != data["version"]:
                return JSONResponse(
                    {
                        "detail": f"Conflict: Task version mismatch. Expected {task['version']}, got {data['version']}",
                        "latest_task": serialize_task(task),
                    },
                    status_code=409,
                )

            # Update fields
            title = data.get("title", task["title"])
            status = data.get("status", task["status"])
            assigned_to = data.get("assigned_to", task["assigned_to"])
            new_version = task["version"] + 1
            now = datetime.now().isoformat()

            cursor.execute(
                """UPDATE tasks SET title = ?, status = ?, assigned_to = ?, version = ?, updated_at = ?
                   WHERE id = ?""",
                (title, status, assigned_to, new_version, now, task_id),
            )
            conn.commit()

            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            updated_task = cursor.fetchone()
            return JSONResponse(serialize_task(updated_task))
    except Exception as e:
        return JSONResponse({"detail": str(e)}, status_code=400)


async def delete_task(request):
    """Delete a task"""
    try:
        task_id = request.path_params["task_id"]
        
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            task = cursor.fetchone()

            if not task:
                return JSONResponse({"detail": "Task not found"}, status_code=404)

            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            return JSONResponse({"message": "Task deleted"})
    except Exception as e:
        return JSONResponse({"detail": str(e)}, status_code=400)


# ============ Health Check ============

async def health_check(request):
    """Health check endpoint"""
    return JSONResponse({"status": "ok", "service": "Collaborative Task Board API"})


# ============ Routes ============

routes = [
    # Users
    Route("/users", create_user, methods=["POST"]),
    Route("/users", get_users, methods=["GET"]),
    # Tasks
    Route("/tasks", create_task, methods=["POST"]),
    Route("/tasks", get_tasks, methods=["GET"]),
    Route("/tasks/{task_id}", update_task, methods=["PUT"]),
    Route("/tasks/{task_id}", delete_task, methods=["DELETE"]),
    # Health
    Route("/health", health_check, methods=["GET"]),
]

# Create app
app = Starlette(routes=routes)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://collaborative-task-board.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
