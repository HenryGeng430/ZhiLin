"""Unified demo response envelope."""
from __future__ import annotations

import secrets


def trace_id() -> str:
    return "tr-" + secrets.token_hex(4)


def ok(data=None, message: str = "") -> dict:
    return {"code": "OK", "message": message, "data": data, "traceId": trace_id()}


def err(code: str, message: str) -> dict:
    return {"code": code, "message": message, "data": None, "traceId": trace_id()}
