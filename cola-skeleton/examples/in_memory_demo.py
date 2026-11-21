"""Small composition root: infrastructure is wired at the edge."""
from __future__ import annotations

from cola_skeleton.adapter.http import make_router
from cola_skeleton.application.use_cases import NoteService
from cola_skeleton.infrastructure.memory import InMemoryNoteRepository


def main() -> None:
    router = make_router(NoteService(InMemoryNoteRepository()))
    status, body = router.dispatch(
        "POST", "/api/v1/notes", {}, {"title": "Architecture note"})
    print(status, body)
    status, body = router.dispatch("GET", "/api/v1/notes", {}, {})
    print(status, body)


if __name__ == "__main__":
    main()
