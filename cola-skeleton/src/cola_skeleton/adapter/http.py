"""Framework-free HTTP adapter for the public COLA skeleton."""
from __future__ import annotations

import re
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any

from cola_skeleton.application.use_cases import NoteService
from cola_skeleton.common.errors import DemoError
from cola_skeleton.common.result import err, ok
from cola_skeleton.domain.model import Note

NOTE_ITEM = re.compile(r"^/api/v1/notes/([^/]+)$")


def _dto(note: Note) -> dict[str, Any]:
    data = asdict(note)
    return {
        "id": data["id"],
        "title": data["title"],
        "body": data["body"],
        "createdAt": data["created_at"],
        "updatedAt": data["updated_at"],
    }


class NoteRouter:
    def __init__(self, service: NoteService) -> None:
        self._service = service

    def dispatch(self, method: str, path: str, query: dict[str, str],
                 body: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        try:
            if method == "GET" and path == "/api/v1/health":
                return 200, ok({
                    "status": "UP",
                    "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                })
            if path == "/api/v1/notes":
                if method == "GET":
                    notes = self._service.list(query.get("limit", 20), query.get("offset", 0))
                    return 200, ok({"items": [_dto(n) for n in notes], "count": len(notes)})
                if method == "POST":
                    note = self._service.create(body.get("title"), body.get("body", ""))
                    return 201, ok(_dto(note))
                return 405, err("METHOD_NOT_ALLOWED", "method not allowed")
            match = NOTE_ITEM.match(path)
            if match:
                note_id = match.group(1)
                if method == "GET":
                    return 200, ok(_dto(self._service.get(note_id)))
                if method == "PATCH":
                    note = self._service.update(note_id, body.get("title"), body.get("body"))
                    return 200, ok(_dto(note))
                if method == "DELETE":
                    self._service.delete(note_id)
                    return 200, ok({"deleted": True})
                return 405, err("METHOD_NOT_ALLOWED", "method not allowed")
            return 404, err("NOT_FOUND", "route not found")
        except DemoError as exc:
            return exc.http, err(exc.code, exc.message)
        except ValueError as exc:
            return 400, err("INVALID_ARGUMENT", str(exc))
        except Exception:
            return 500, err("INTERNAL_ERROR", "internal error")


def make_router(service: NoteService) -> NoteRouter:
    return NoteRouter(service)
