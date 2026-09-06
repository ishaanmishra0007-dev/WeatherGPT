import sqlite3
from pathlib import Path


# Store the database inside the backend folder
DATABASE_PATH = Path(__file__).resolve().parent.parent / "weathergpt.db"


def get_connection():
    """Create and return a connection to the SQLite database."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Create the recommendations table if it does not already exist."""
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity TEXT NOT NULL,
            date TEXT NOT NULL,
            best_time TEXT,
            score INTEGER,
            risk TEXT,
            window_start TEXT,
            window_end TEXT,
            window_duration REAL,
            average_score INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()

def save_recommendation(recommendation):
    connection = get_connection()

    window = recommendation.get("best_window")

    connection.execute("""
        INSERT INTO recommendations (
            activity,
            date,
            best_time,
            score,
            risk,
            window_start,
            window_end,
            window_duration,
            average_score
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        recommendation["activity"],
        recommendation["date"],
        recommendation.get("best_time"),
        recommendation.get("score"),
        recommendation.get("risk"),
        window.get("start") if window else None,
        window.get("end") if window else None,
        window.get("duration") if window else None,
        window.get("average_score") if window else None
    ))

    connection.commit()
    connection.close()