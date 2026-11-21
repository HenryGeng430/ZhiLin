"""SQLite adapter: parameterized SQL, no ORM, easy to inspect."""
from __future__ import annotations

import sqlite3
from pathlib import Path

from domain.model import Note

SCHEMA = """
CREATE TABLE IF NOT EXISTS notes (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  body TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
"""


class SqliteNoteRepository:
    def __init__(self, path: str | Path) -> None:
        self.path = str(path)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.executescript(SCHEMA)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path, timeout=10)
        conn.row_factory = sqlite3.Row
        return conn

    def save(self, note: Note) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO notes(id,title,body,created_at,updated_at) VALUES(?,?,?,?,?) "
                "ON CONFLICT(id) DO UPDATE SET title=excluded.title, body=excluded.body, "
                "updated_at=excluded.updated_at",
                (note.id, note.title, note.body, note.created_at, note.updated_at),
            )

    def get(self, note_id: str) -> Note | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
        return _row(row) if row else None

    def list(self) -> list[Note]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM notes").fetchall()
        return [_row(r) for r in rows]

    def delete(self, note_id: str) -> bool:
        with self._connect() as conn:
            cur = conn.execute("DELETE FROM notes WHERE id=?", (note_id,))
            return cur.rowcount > 0


def _row(row: sqlite3.Row) -> Note:
    return Note(
        id=row["id"], title=row["title"], body=row["body"],
        created_at=row["created_at"], updated_at=row["updated_at"],
    )
