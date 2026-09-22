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