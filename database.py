
import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from contextlib import contextmanager

DB_PATH = Path(__file__).parent / "careerpilot.db"

VALID_STATUSES = {
    "Applied",
    "Shortlisted",
    "Interview",
    "Selected",
    "Rejected",
    "Withdrawn"
}


@contextmanager
def get_connection():
    """Create and safely close a database connection."""

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database():
    """Create the applications table if it doesn't exist."""

    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                role TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Applied',
                applied_at TEXT NOT NULL
            )
        """)


def add_application(company: str, role: str, status: str = "Applied"):
    """Insert a new application."""

    company = company.strip()
    role = role.strip()

    if not company or not role:
        raise ValueError("Company and role cannot be empty.")

    if status not in VALID_STATUSES:
        raise ValueError("Invalid application status.")

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO applications
            (company, role, status, applied_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                company,
                role,
                status,
                datetime.now(timezone.utc).isoformat()
            )
        )

        return cursor.lastrowid


def get_applications(status: str | None = None):
    """Retrieve applications, optionally filtered by status."""

    if status and status not in VALID_STATUSES:
        raise ValueError("Invalid application status.")

    with get_connection() as connection:

        if status:
            rows = connection.execute(
                """
                SELECT * FROM applications
                WHERE status = ?
                ORDER BY id DESC
                """,
                (status,)
            ).fetchall()

        else:
            rows = connection.execute(
                """
                SELECT * FROM applications
                ORDER BY id DESC
                """
            ).fetchall()

        return [dict(row) for row in rows]


def search_applications(keyword: str):
    """Search applications by company or role."""

    keyword = keyword.strip()

    if not keyword:
        raise ValueError("Search keyword cannot be empty.")

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT * FROM applications
            WHERE company LIKE ? OR role LIKE ?
            ORDER BY id DESC
            """,
            (f"%{keyword}%", f"%{keyword}%")
        ).fetchall()

        return [dict(row) for row in rows]


def update_application(application_id: int, status: str):
    """Update the status of an application."""

    if application_id <= 0:
        raise ValueError("Application ID must be positive.")

    if status not in VALID_STATUSES:
        raise ValueError("Invalid application status.")

    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE applications
            SET status = ?
            WHERE id = ?
            """,
            (status, application_id)
        )

        return cursor.rowcount > 0


def get_application_stats():
    """Return application statistics grouped by status."""

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT status, COUNT(*) AS total
            FROM applications
            GROUP BY status
            """
        ).fetchall()

        statistics = {
            status: 0 for status in VALID_STATUSES
        }

        for row in rows:
            statistics[row["status"]] = row["total"]

        return {
            "total_applications": sum(statistics.values()),
            "by_status": statistics
        }
