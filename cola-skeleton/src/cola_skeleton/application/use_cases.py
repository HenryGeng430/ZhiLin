"""Application use cases depend on ports, never on infrastructure."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from cola_skeleton.common.errors import DemoError
from cola_skeleton.domain.model import Note
from cola_skeleton.domain.ports import NoteRepository


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class NoteService:
    def __init__(self, repository: NoteRepository) -> None:
        self._repository = repository

    def create(self, title: str, body: str = "") -> Note:
        title = str(title or "").strip()
        if not title:
            raise DemoError("INVALID_ARGUMENT", "title is required", 400)
        now = _now()
        note = Note(uuid.uuid4().hex[:12], title[:120], str(body or "")[:4000], now, now)
        self._repository.save(note)
        return note

    def get(self, note_id: str) -> Note:
        note = self._repository.get(note_id)
        if note is None:
            raise DemoError("NOT_FOUND", "note not found", 404)
        return note

    def update(self, note_id: str, title: str | None = None,
               body: str | None = None) -> Note:
        note = self.get(note_id)
        try:
            updated = note.edit(title, body, _now())
        except ValueError as exc:
            raise DemoError("INVALID_ARGUMENT", str(exc), 400) from exc
        self._repository.save(updated)
        return updated

    def delete(self, note_id: str) -> None:
        if not self._repository.delete(note_id):
            raise DemoError("NOT_FOUND", "note not found", 404)

    def list(self, limit: int = 20, offset: int = 0) -> list[Note]:
        try:
            limit = max(1, min(100, int(limit)))
            offset = max(0, int(offset))
        except (TypeError, ValueError) as exc:
            raise DemoError("INVALID_ARGUMENT", "invalid pagination", 400) from exc
        items = sorted(self._repository.list(), key=lambda n: (n.updated_at, n.id), reverse=True)
        return items[offset:offset + limit]
