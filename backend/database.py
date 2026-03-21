import sqlite3
import os
from contextlib import contextmanager

DATABASE_PATH = "tasks.db"


def init_db():
    """Initialize database with tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'TODO',
            assigned_to TEXT,
            updated_at TEXT NOT NULL,
            version INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (assigned_to) REFERENCES users(id)
        )
    """
    )

    conn.commit()
    conn.close()


@contextmanager
def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


# Initialize on import
init_db()
