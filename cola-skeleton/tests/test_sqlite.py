from __future__ import annotations

import os
import tempfile
import unittest

from domain.model import Note
from infrastructure.sqlite import SqliteNoteRepository


class SqliteRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="cola-sqlite-")
        self.repo = SqliteNoteRepository(os.path.join(self.tmp, "notes.db"))

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

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
