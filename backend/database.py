import psycopg2
from psycopg2 import sql
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://neondb_owner:password@ep-nameless-wave-am80yc5s-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)


def init_db():
    """Initialize database with tables"""
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


@contextmanager
def get_db():
    """Get database connection"""
    conn = psycopg2.connect(DATABASE_URL)
    conn.set_session(autocommit=False)
    
    # Create a cursor with row factory-like behavior
    cursor = conn.cursor()
    
    try:
        yield conn
    finally:
        cursor.close()
        conn.close()


# Initialize on import
try:
    init_db()
except Exception as e:
    print(f"Database initialization error: {e}")
