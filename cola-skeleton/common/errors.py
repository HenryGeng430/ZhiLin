"""Stable demo errors for the public skeleton."""
from __future__ import annotations


class DemoError(Exception):
    def __init__(self, code: str, message: str, http: int = 400) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.http = http
