"""SQLite adapter tests use a temporary database."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from cola_skeleton.domain.model import Note
from cola_skeleton.infrastructure.sqlite import SqliteNoteRepository


class SqliteRepositoryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="cola-sqlite-")
        self.repo = SqliteNoteRepository(Path(self.tmp.name) / "notes.db")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_round_trip_and_update(self):
        note = Note("n1", "Title", "Body", "2026-01-01T00:00:00", "2026-01-01T00:00:00")
        self.repo.save(note)
        self.assertEqual(self.repo.get("n1").title, "Title")
        self.repo.save(Note("n1", "New", "Body", note.created_at, "2026-01-02T00:00:00"))
        self.assertEqual(self.repo.get("n1").title, "New")
        self.assertEqual(len(self.repo.list()), 1)
        self.assertTrue(self.repo.delete("n1"))
        self.assertIsNone(self.repo.get("n1"))


if __name__ == "__main__":
    unittest.main()
