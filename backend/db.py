import sqlite3
import json
from datetime import date
from typing import Optional

DB_PATH = "journal.db"


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't exist."""
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                content  TEXT    NOT NULL,
                date     TEXT    NOT NULL,
                insights TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.commit()


def _row_to_dict(row) -> dict:
    d = dict(row)
    if d.get("insights") and isinstance(d["insights"], str):
        try:
            d["insights"] = json.loads(d["insights"])
        except json.JSONDecodeError:
            pass
    return d


def create_entry(content: str, entry_date: Optional[str] = None) -> dict:
    today = entry_date or date.today().isoformat()
    with _connect() as conn:
        cursor = conn.execute(
            "INSERT INTO entries (content, date) VALUES (?, ?)",
            (content, today),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM entries WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
    return _row_to_dict(row)


def get_all_entries() -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM entries ORDER BY created_at DESC"
        ).fetchall()
    return [_row_to_dict(r) for r in rows]


def get_entry(entry_id: int) -> Optional[dict]:
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM entries WHERE id = ?", (entry_id,)
        ).fetchone()
    return _row_to_dict(row) if row else None


def save_insights(entry_id: int, insights: dict):
    with _connect() as conn:
        conn.execute(
            "UPDATE entries SET insights = ? WHERE id = ?",
            (json.dumps(insights), entry_id),
        )
        conn.commit()


def delete_entry(entry_id: int) -> bool:
    with _connect() as conn:
        cursor = conn.execute(
            "DELETE FROM entries WHERE id = ?", (entry_id,)
        )
        conn.commit()
    return cursor.rowcount > 0
