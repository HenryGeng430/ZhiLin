"""Domain model tests: pure rules, no HTTP or database."""
from __future__ import annotations

import unittest

from cola_skeleton.domain.model import Note


class NoteModelTest(unittest.TestCase):
    def test_rename_trims_and_caps_title(self):
        note = Note("n1", "Old")
        renamed = note.rename("  New title  ", "2026-01-01T00:00:00")
        self.assertEqual(renamed.title, "New title")
        self.assertEqual(renamed.updated_at, "2026-01-01T00:00:00")

    def test_rename_rejects_blank_title(self):
        with self.assertRaises(ValueError):
            Note("n1", "Old").rename("   ")

    def test_edit_keeps_unspecified_fields(self):
        note = Note("n1", "Title", "Body", "created", "updated")
        edited = note.edit(body="New body", updated_at="later")
        self.assertEqual(edited.title, "Title")
        self.assertEqual(edited.body, "New body")
        self.assertEqual(edited.created_at, "created")
        self.assertEqual(edited.updated_at, "later")

    def test_edit_caps_body(self):
        note = Note("n1", "Title").edit(body="x" * 5000)
        self.assertEqual(len(note.body), 4000)


if __name__ == "__main__":
    unittest.main()
