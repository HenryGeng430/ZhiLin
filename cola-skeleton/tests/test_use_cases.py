"""Application tests use a fake port, not a real database."""
from __future__ import annotations

import unittest

from cola_skeleton.application.use_cases import NoteService
from cola_skeleton.common.errors import DemoError
from cola_skeleton.domain.model import Note


class FakeRepo:
    def __init__(self) -> None:
        self.items: dict[str, Note] = {}

    def save(self, note: Note) -> None:
        self.items[note.id] = note

    def get(self, note_id: str) -> Note | None:
        return self.items.get(note_id)

    def list(self) -> list[Note]:
        return list(self.items.values())

    def delete(self, note_id: str) -> bool:
        return self.items.pop(note_id, None) is not None


class NoteServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.service = NoteService(FakeRepo())

    def test_create_requires_title(self):
        with self.assertRaises(DemoError) as ctx:
            self.service.create("  ")
        self.assertEqual(ctx.exception.code, "INVALID_ARGUMENT")

    def test_crud(self):
        note = self.service.create("Demo", "body")
        self.assertEqual(self.service.get(note.id).title, "Demo")
        updated = self.service.update(note.id, title="Renamed")
        self.assertEqual(updated.title, "Renamed")
        self.assertEqual(self.service.list()[0].title, "Renamed")
        self.service.delete(note.id)
        with self.assertRaises(DemoError) as ctx:
            self.service.get(note.id)
        self.assertEqual(ctx.exception.http, 404)

    def test_list_clamps_pagination(self):
        for index in range(3):
            self.service.create(f"Note {index}")
        self.assertEqual(len(self.service.list(limit=2, offset=0)), 2)
        self.assertEqual(len(self.service.list(limit=999, offset=0)), 3)


if __name__ == "__main__":
    unittest.main()
