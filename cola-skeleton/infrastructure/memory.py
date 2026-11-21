"""In-memory adapter implementing the domain port."""
from __future__ import annotations

from domain.model import Note


class InMemoryNoteRepository:
    def __init__(self) -> None:
        self._items: dict[str, Note] = {}

    def save(self, note: Note) -> None:
        self._items[note.id] = note

    def get(self, note_id: str) -> Note | None:
        return self._items.get(note_id)

    def list(self) -> list[Note]:
        return list(self._items.values())

    def delete(self, note_id: str) -> bool:
        return self._items.pop(note_id, None) is not None
