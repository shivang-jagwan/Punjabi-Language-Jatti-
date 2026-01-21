#!/usr/bin/env python3
"""Jatti Playground server.

- Serves the static UI from ./frontend
- Exposes POST /api/run to execute Jatti code without writing files

Run:
  python playground_server.py
Then open:
  http://127.0.0.1:8000/

Security:
  This runs code on your machine. Keep it bound to localhost.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import subprocess
import sys
import time
from collections import deque
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parent
FRONTEND_DIR = REPO_ROOT / "frontend"
WORKER_PY = REPO_ROOT / "playground_worker.py"


def _load_dotenv(dotenv_path: Path) -> None:
    """Load a minimal .env file.

    - Lines like KEY=VALUE
    - Ignores blank lines and comments starting with '#'
    - Environment variables already set take precedence
    """

    if not dotenv_path.exists() or not dotenv_path.is_file():
        return

    try:
        for raw_line in dotenv_path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("\"").strip("'")
            if not key:
                continue
            os.environ.setdefault(key, value)
    except Exception:
        # Intentionally ignore dotenv parsing issues.
        return


def _get_env_int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, str(default)).strip())
    except Exception:
        return default


_load_dotenv(REPO_ROOT / ".env")

JATTI_API_KEY = os.environ.get("JATTI_API_KEY", "").strip()
MAX_CODE_BYTES = _get_env_int("JATTI_MAX_CODE_BYTES", 200_000)
MAX_OUTPUT_BYTES = _get_env_int("JATTI_MAX_OUTPUT_BYTES", 200_000)
RUN_TIMEOUT_SEC = float(os.environ.get("JATTI_TIMEOUT_SEC", "2.5").strip() or 2.5)

# Simple fixed-window rate limiting: N requests per window seconds, per IP
RATE_WINDOW_SEC = float(os.environ.get("JATTI_RATE_WINDOW_SEC", "10").strip() or 10)
RATE_MAX_REQ = _get_env_int("JATTI_RATE_MAX_REQ", 30)
_RATE: dict[str, deque[float]] = {}


def _client_ip(handler: BaseHTTPRequestHandler) -> str:
    # If you run behind a reverse proxy, set it up to pass X-Forwarded-For.
    xff = handler.headers.get("X-Forwarded-For")
    if xff:
        return xff.split(",", 1)[0].strip()
    return handler.client_address[0]


def _rate_ok(ip: str) -> bool:
    now = time.time()
    q = _RATE.get(ip)
    if q is None:
        q = deque()
        _RATE[ip] = q
    # Drop old timestamps
    while q and (now - q[0]) > RATE_WINDOW_SEC:
        q.popleft()
    if len(q) >= RATE_MAX_REQ:
        return False
    q.append(now)
    return True


def _run_jatti_subprocess(code: str) -> tuple[bool, str, bool, bool]:
    """Run Jatti code in a subprocess.

    Returns: (success, output, timed_out, truncated)
    """
    if not WORKER_PY.exists():
        return False, "Server misconfigured: playground_worker.py missing", False, False

    proc = subprocess.Popen(
        [sys.executable, str(WORKER_PY)],
        cwd=str(REPO_ROOT),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    assert proc.stdin is not None
    assert proc.stdout is not None

    timed_out = False
    truncated = False
    out_chunks: list[str] = []
    out_len = 0

    try:
        proc.stdin.write(code)
        proc.stdin.close()

        start = time.time()
        # Read output incrementally so we can cap size
        while True:
            if proc.poll() is not None:
                # Drain remaining output
                remainder = proc.stdout.read()
                if remainder:
                    take = remainder
                    if out_len + len(take.encode("utf-8", "ignore")) > MAX_OUTPUT_BYTES:
                        # Approx cap: slice by characters; good enough for UI
                        truncated = True
                        take = take[: max(0, MAX_OUTPUT_BYTES - out_len)]
                    out_chunks.append(take)
                break

            if time.time() - start > RUN_TIMEOUT_SEC:
                timed_out = True
                proc.kill()
                break

            chunk = proc.stdout.read(1024)
            if chunk:
                chunk_bytes = len(chunk.encode("utf-8", "ignore"))
                if out_len + chunk_bytes > MAX_OUTPUT_BYTES:
                    truncated = True
                    # Add only what fits
                    remaining = max(0, MAX_OUTPUT_BYTES - out_len)
                    if remaining:
                        out_chunks.append(chunk[:remaining])
                    proc.kill()
                    break
                out_len += chunk_bytes
                out_chunks.append(chunk)
            else:
                time.sleep(0.01)

        output = "".join(out_chunks)
    finally:
        try:
            proc.kill()
        except Exception:
            pass

    # Heuristic: roast_error prints a banner containing "❌ JATTI ERROR"
    success = (not timed_out) and ("❌ JATTI ERROR" not in output)
    if timed_out:
        output = (output + "\n" if output else "") + f"⏱️ Timed out after {RUN_TIMEOUT_SEC}s"
        success = False
    if truncated:
        output = (output + "\n" if output else "") + "…(output truncated)"

    return success, output, timed_out, truncated


def _read_json(handler: BaseHTTPRequestHandler) -> dict:
    length = int(handler.headers.get("Content-Length", "0"))
    if length > MAX_CODE_BYTES:
        return {"__too_large__": True}

    raw = handler.rfile.read(length) if length else b"{}"
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception:
        return {}


class PlaygroundHandler(BaseHTTPRequestHandler):
    server_version = "JattiPlayground/0.1"

    def _send_json(self, status: int, payload: dict) -> None:
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_file(self, file_path: Path) -> None:
        if not file_path.exists() or not file_path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        ctype, _ = mimetypes.guess_type(str(file_path))
        ctype = ctype or "application/octet-stream"
        data = file_path.read_bytes()

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/healthz":
            return self._send_json(HTTPStatus.OK, {"ok": True})

        if path == "/" or path == "":
            return self._send_file(FRONTEND_DIR / "index.html")

        if path.startswith("/assets/"):
            rel = path.removeprefix("/")
            return self._send_file(FRONTEND_DIR / rel)

        self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/api/run":
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        ip = _client_ip(self)
        if not _rate_ok(ip):
            self._send_json(HTTPStatus.TOO_MANY_REQUESTS, {"success": False, "error": "Rate limit exceeded"})
            return

        if JATTI_API_KEY:
            provided = (self.headers.get("X-API-Key") or "").strip()
            if provided != JATTI_API_KEY:
                self._send_json(HTTPStatus.UNAUTHORIZED, {"success": False, "error": "Unauthorized"})
                return

        body = _read_json(self)
        if body.get("__too_large__"):
            self._send_json(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"success": False, "error": "Code too large"})
            return

        code = body.get("code", "")
        if not isinstance(code, str) or not code.strip():
            self._send_json(HTTPStatus.BAD_REQUEST, {"success": False, "error": "Missing code"})
            return

        success, output, timed_out, truncated = _run_jatti_subprocess(code)
        self._send_json(
            HTTPStatus.OK,
            {
                "success": success,
                "output": output,
                "timedOut": timed_out,
                "truncated": truncated,
            },
        )

    def log_message(self, format, *args):
        # Keep console clean; uncomment for debugging.
        return


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    if not FRONTEND_DIR.exists():
        print(f"frontend/ not found at {FRONTEND_DIR}")
        return 1

    os.chdir(str(REPO_ROOT))

    httpd = ThreadingHTTPServer((args.host, args.port), PlaygroundHandler)
    print(f"Jatti Playground running at http://{args.host}:{args.port}/")
    print("Press Ctrl+C to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
