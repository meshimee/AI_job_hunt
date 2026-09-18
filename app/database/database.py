import sqlite3
from pathlib import Path


# Store our database inside the project's data folder
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_PATH = PROJECT_ROOT / "data" / "jobhunt.db"


def get_connection():
    """Create and return a connection to the JobHunt AI database."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    # Allows us to access database columns by name
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """Create the database tables if they don't already exist."""

    connection = get_connection()

    cursor = connection.cursor()

    # Main job/opportunity table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS opportunities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT,
            contact_name TEXT,
            contact_role TEXT,
            source TEXT,
            stage TEXT,
            status TEXT,
            priority TEXT,
            deadline TEXT,
            next_action TEXT,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tasks related to opportunities
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            opportunity_id INTEGER,
            task TEXT NOT NULL,
            deadline TEXT,
            priority TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (opportunity_id)
                REFERENCES opportunities(id)
        )
    """)

    # Messages/interactions with recruiters, hiring managers, etc.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            opportunity_id INTEGER,
            channel TEXT,
            direction TEXT,
            message TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (opportunity_id)
                REFERENCES opportunities(id)
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()
    print("JobHunt AI database initialized successfully.")