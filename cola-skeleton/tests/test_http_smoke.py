"""End-to-end smoke test: start the real server and call the HTTP API."""
from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def call(method: str, url: str, body: dict | None = None):
    data = None if body is None else json.dumps(body).encode()
    request = urllib.request.Request(url, data=data, method=method)
    request.add_header("Accept", "application/json")
    if data is not None:
        request.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status, json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode())


class HttpSmokeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="cola-http-")
        self.port = free_port()
        env = os.environ.copy()
        env["PYTHONPATH"] = str(ROOT / "src")
        self.proc = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "cola_skeleton.server",
                "--port",
                str(self.port),
                "--db",
                str(Path(self.tmp.name) / "notes.db"),
            ],
            cwd=ROOT,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        deadline = time.time() + 8
        while time.time() < deadline:
            try:
                status, _ = call("GET", f"http://127.0.0.1:{self.port}/api/v1/health")
                if status == 200:
                    break
            except Exception:
                time.sleep(0.2)
        else:
            self.fail("server did not start")

    def tearDown(self) -> None:
        self.proc.terminate()
        try:
            self.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.proc.kill()
        self.tmp.cleanup()

    def test_note_crud(self):
        base = f"http://127.0.0.1:{self.port}/api/v1/notes"
        status, body = call("POST", base, {"title": "Hello", "body": "World"})
        self.assertEqual(status, 201)
        note_id = body["data"]["id"]
        status, body = call("GET", base + "/" + note_id)
        self.assertEqual(status, 200)
        self.assertEqual(body["data"]["title"], "Hello")
        status, body = call("PATCH", base + "/" + note_id, {"title": "Changed"})
        self.assertEqual(status, 200)
        self.assertEqual(body["data"]["title"], "Changed")
        status, _ = call("DELETE", base + "/" + note_id)
        self.assertEqual(status, 200)
        status, _ = call("GET", base + "/" + note_id)
        self.assertEqual(status, 404)


if __name__ == "__main__":
    unittest.main()
