from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def call(method, url, body=None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Accept", "application/json")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())


class HttpSmokeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="cola-http-")
        self.port = free_port()
        self.proc = subprocess.Popen(
            [sys.executable, os.path.join(ROOT, "server.py"),
             "--port", str(self.port), "--db", os.path.join(self.tmp, "notes.db")],
            cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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

    def tearDown(self):
        self.proc.terminate()
        try:
            self.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.proc.kill()
        shutil.rmtree(self.tmp, ignore_errors=True)

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
        status, body = call("DELETE", base + "/" + note_id)
        self.assertEqual(status, 200)
        status, body = call("GET", base + "/" + note_id)
        self.assertEqual(status, 404)


if __name__ == "__main__":
    unittest.main()
