"""Pure domain model: a generic note, not a ZhiLin business entity."""
from __future__ import annotations

from dataclasses import dataclass, replace


@dataclass(frozen=True, slots=True)
class Note:
    id: str
    title: str
    body: str = ""
    created_at: str = ""
    updated_at: str = ""

    def rename(self, title: str, updated_at: str = "") -> "Note":
        title = title.strip()
        if not title:
            raise ValueError("title is required")
        return replace(self, title=title[:120], updated_at=updated_at or self.updated_at)

    def edit(self, title: str | None = None, body: str | None = None,
             updated_at: str = "") -> "Note":
        title = self.title if title is None else str(title).strip()[:120]
        if not title:
            raise ValueError("title is required")
        body = self.body if body is None else str(body)[:4000]
        return replace(self, title=title, body=body, updated_at=updated_at or self.updated_at)
