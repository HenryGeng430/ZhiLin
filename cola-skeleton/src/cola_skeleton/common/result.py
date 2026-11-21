"""Unified demo response envelope."""
from __future__ import annotations

import secrets
from typing import Any


def trace_id() -> str:
    return "tr-" + secrets.token_hex(4)


def ok(data: Any = None, message: str = "") -> dict[str, Any]:
    return {"code": "OK", "message": message, "data": data, "traceId": trace_id()}


def err(code: str, message: str) -> dict[str, Any]:
    return {"code": code, "message": message, "data": None, "traceId": trace_id()}
