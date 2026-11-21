from __future__ import annotations

import unittest

from application.use_cases import NoteService
from common.errors import DemoError
from domain.model import Note


class FakeRepo:
    def __init__(self):
        self.items: dict[str, Note] = {}

    def save(self, note):
        self.items[note.id] = note

    def get(self, note_id):
        return self.items.get(note_id)

    def list(self):
        return list(self.items.values())

    def delete(self, note_id):
        return self.items.pop(note_id, None) is not None


class NoteServiceTest(unittest.TestCase):
    def setUp(self):
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


if __name__ == "__main__":
    unittest.main()
