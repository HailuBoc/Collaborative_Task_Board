import os
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Determine if using PostgreSQL or SQLite
USE_POSTGRES = DATABASE_URL and DATABASE_URL.startswith("postgresql")

if USE_POSTGRES:
    import psycopg2
else:
    import sqlite3
    if not DATABASE_URL:
        DATABASE_URL = "sqlite:///tasks.db"


def init_db():
    """Initialize database with tables"""
    try:
        if USE_POSTGRES:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id VARCHAR(36) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id VARCHAR(36) PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    status VARCHAR(50) NOT NULL DEFAULT 'TODO',
                    assigned_to VARCHAR(36),
                    updated_at TIMESTAMP NOT NULL,
                    version INTEGER NOT NULL DEFAULT 1,
                    FOREIGN KEY (assigned_to) REFERENCES users(id) ON DELETE SET NULL
                )
            """)

            conn.commit()
            cursor.close()
            conn.close()
        else:
            # SQLite
            db_path = DATABASE_URL.replace("sqlite:///", "")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'TODO',
                    assigned_to TEXT,
                    updated_at TEXT NOT NULL,
                    version INTEGER NOT NULL DEFAULT 1,
                    FOREIGN KEY (assigned_to) REFERENCES users(id) ON DELETE SET NULL
                )
            """)

            conn.commit()
            cursor.close()
            conn.close()
    except Exception as e:
        print(f"Database init error: {e}")


@contextmanager
def get_db():
    """Get database connection"""
    if USE_POSTGRES:
        conn = psycopg2.connect(DATABASE_URL)
    else:
        db_path = DATABASE_URL.replace("sqlite:///", "")
        conn = sqlite3.connect(db_path)
    
    try:
        yield conn
    finally:
        conn.close()
