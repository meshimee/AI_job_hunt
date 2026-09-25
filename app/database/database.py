import sqlite3
from pathlib import Path


# ---------------------------------------------------------
# Database Configuration
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_PATH = PROJECT_ROOT / "data" / "jobhunt.db"


# ---------------------------------------------------------
# Database Connection
# ---------------------------------------------------------

def get_connection():
    """
    Create and return a connection to the JobHunt AI database.
    """

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(DATABASE_PATH)

    # Allows rows to be accessed by column name
    connection.row_factory = sqlite3.Row

    return connection


# ---------------------------------------------------------
# Database Initialization
# ---------------------------------------------------------

def initialize_database():
    """
    Create all required database tables if they do not exist.
    """

    connection = get_connection()

    cursor = connection.cursor()

    # -----------------------------------------------------
    # Opportunities
    # -----------------------------------------------------

    cursor.execute(
        """
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
        """
    )

    # -----------------------------------------------------
    # Tasks
    # -----------------------------------------------------

    cursor.execute(
        """
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
        """
    )

    # -----------------------------------------------------
    # Interactions
    # -----------------------------------------------------

    cursor.execute(
        """
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
        """
    )

    connection.commit()

    connection.close()


# ---------------------------------------------------------
# Run directly
# ---------------------------------------------------------

if __name__ == "__main__":

    initialize_database()

    print(
        "JobHunt AI database initialized successfully."
    )