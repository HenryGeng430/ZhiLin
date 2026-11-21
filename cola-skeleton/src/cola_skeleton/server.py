"""Composition root and standard-library HTTP transport.

Run:
    python -m cola_skeleton.server --port 8098 --db ./notes.db

This is a generic Note CRUD demo. It intentionally contains no product
business logic, prompts, course model, mastery policy or quota rules.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from cola_skeleton.adapter.http import NoteRouter, make_router
from cola_skeleton.application.use_cases import NoteService
from cola_skeleton.common.result import err
from cola_skeleton.infrastructure.sqlite import SqliteNoteRepository


class Handler(BaseHTTPRequestHandler):
    server_version = "ZhiLinColaDemo/1.0"
    protocol_version = "HTTP/1.1"
    router: NoteRouter | None = None

    def log_message(self, fmt: str, *args: object) -> None:
        if os.environ.get("DEMO_VERBOSE"):
            sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def _cors(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,PATCH,DELETE,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type,Accept")

    def _send(self, status: int, payload: dict[str, Any]) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self._cors()
        self.end_headers()
        try:
            self.wfile.write(data)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _handle(self, method: str) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = urllib.parse.unquote(parsed.path)
        query = {k: v[0] for k, v in urllib.parse.parse_qs(parsed.query).items()}
        body: dict[str, Any] = {}
        length = int(self.headers.get("Content-Length") or 0)
        if length:
            if length > 1024 * 1024:
                return self._send(413, err("PAYLOAD_TOO_LARGE", "body too large"))
            raw = self.rfile.read(length)
            try:
                body = json.loads(raw.decode("utf-8"))
            except (ValueError, UnicodeDecodeError):
                return self._send(400, err("INVALID_JSON", "invalid JSON body"))
            if not isinstance(body, dict):
                return self._send(400, err("INVALID_JSON", "body must be an object"))
        if self.router is None:
            return self._send(500, err("NOT_READY", "router is not configured"))
        status, payload = self.router.dispatch(method, path, query, body)
        return self._send(status, payload)

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Content-Length", "0")
        self._cors()
        self.end_headers()

    def do_GET(self) -> None:
        self._handle("GET")

    def do_POST(self) -> None:
        self._handle("POST")

    def do_PATCH(self) -> None:
        self._handle("PATCH")

    def do_DELETE(self) -> None:
        self._handle("DELETE")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8098)
    ap.add_argument("--db", default=os.path.join(os.path.dirname(__file__), "notes.db"))
    args = ap.parse_args()

    service = NoteService(SqliteNoteRepository(args.db))
    Handler.router = make_router(service)
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"COLA skeleton demo: http://{args.host}:{args.port}")
    print(f"SQLite: {os.path.abspath(args.db)}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
