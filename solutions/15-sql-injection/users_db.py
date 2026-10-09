"""users_db.py: user lookups."""
import sqlite3
from typing import List, Tuple


def find_users(conn: sqlite3.Connection, name: str) -> List[Tuple[int, str]]:
    """Return (id, name) rows whose name matches `name` exactly."""
    return conn.execute("SELECT id, name FROM users WHERE name = ?", (name,)).fetchall()
