import psycopg2
from psycopg2 import sql
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")


def init_db():
    """Initialize database with tables"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            )
        """)

        # Create tasks table
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
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"✗ Database initialization error: {e}")
        raise


@contextmanager
def get_db():
    """Get database connection"""
    conn = psycopg2.connect(DATABASE_URL)
    conn.set_session(autocommit=False)
    
    try:
        yield conn
    finally:
        conn.close()


# Initialize on import
try:
    init_db()
except Exception as e:
    print(f"Warning: Database initialization failed: {e}")
