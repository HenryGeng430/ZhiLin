"""Public COLA skeleton HTTP server (standard library only).

Run:
    python server.py --port 8098 --db ./notes.db

This is a generic Note CRUD demo. It intentionally contains no ZhiLin
business logic, prompts, course model, mastery policy or quota rules.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from adapter.http import make_router  # noqa: E402
from application.use_cases import NoteService  # noqa: E402
from common.result import err  # noqa: E402
from infrastructure.sqlite import SqliteNoteRepository  # noqa: E402


class Handler(BaseHTTPRequestHandler):
    server_version = "ZhiLinColaDemo/1.0"
    protocol_version = "HTTP/1.1"
    router = None

    def log_message(self, fmt, *args):
        if os.environ.get("DEMO_VERBOSE"):
            sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,PATCH,DELETE,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type,Accept")

    def _send(self, status: int, payload: dict):
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

    def _handle(self, method: str):
        parsed = urllib.parse.urlparse(self.path)
        path = urllib.parse.unquote(parsed.path)
        query = {k: v[0] for k, v in urllib.parse.parse_qs(parsed.query).items()}
        body = {}
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
        status, payload = self.router.dispatch(method, path, query, body)
        return self._send(status, payload)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Content-Length", "0")
        self._cors()
        self.end_headers()

    def do_GET(self):
        self._handle("GET")

    def do_POST(self):
        self._handle("POST")

    def do_PATCH(self):
        self._handle("PATCH")

    def do_DELETE(self):
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
