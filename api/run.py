from __future__ import annotations

import json
import os
import signal
import time
from contextlib import redirect_stderr, redirect_stdout
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from io import StringIO
from urllib.parse import urlparse


def _get_env_int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, str(default)).strip())
    except Exception:
        return default


def _json_response(handler: BaseHTTPRequestHandler, status: int, payload: dict) -> None:
    data = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(data)))
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(data)


class _Timeout(Exception):
    pass


class _alarm:
    def __init__(self, seconds: float):
        self.seconds = max(0.0, float(seconds))
        self._enabled = False
        self._old_handler = None

    def __enter__(self):
        # Vercel runs Python on Linux; SIGALRM should be available.
        if self.seconds <= 0:
            return self
        if not hasattr(signal, "SIGALRM"):
            return self

        def _handle(signum, frame):
            raise _Timeout()

        self._old_handler = signal.getsignal(signal.SIGALRM)
        signal.signal(signal.SIGALRM, _handle)
        try:
            signal.setitimer(signal.ITIMER_REAL, self.seconds)
            self._enabled = True
        except Exception:
            # If alarm isn't supported, just proceed without it.
            self._enabled = False
        return self

    def __exit__(self, exc_type, exc, tb):
        if self._enabled and hasattr(signal, "SIGALRM"):
            try:
                signal.setitimer(signal.ITIMER_REAL, 0)
            except Exception:
                pass
            try:
                if self._old_handler is not None:
                    signal.signal(signal.SIGALRM, self._old_handler)
            except Exception:
                pass
        return False


def _run_jatti(code: str) -> tuple[bool, str, bool, bool]:
    # Import here so the function cold-start can bundle correctly.
    from compiler.core import run as jatti_run

    timeout_sec = float(os.environ.get("JATTI_TIMEOUT_SEC", "2.5").strip() or 2.5)
    max_output_bytes = _get_env_int("JATTI_MAX_OUTPUT_BYTES", 200_000)

    buf = StringIO()
    started = time.time()
    timed_out = False

    try:
        with _alarm(timeout_sec):
            with redirect_stdout(buf), redirect_stderr(buf):
                jatti_run(code)
    except _Timeout:
        timed_out = True
        buf.write(f"\n\u23f1\ufe0f Timed out after {timeout_sec}s")
    except Exception as e:
        # Keep response stable; the interpreter typically prints its own errors.
        buf.write(f"\nUnhandled server error: {e}")

    output = buf.getvalue()

    truncated = False
    out_bytes = output.encode("utf-8", "ignore")
    if len(out_bytes) > max_output_bytes:
        truncated = True
        # Slice by bytes (utf-8 safe enough for ASCII output).
        output = out_bytes[:max_output_bytes].decode("utf-8", "ignore") + "\n\u2026(output truncated)"

    # Heuristic: roast_error prints a banner containing "❌ JATTI ERROR"
    success = (not timed_out) and ("\u274c JATTI ERROR" not in output)

    # Add timing (useful in serverless logs)
    elapsed_ms = int((time.time() - started) * 1000)
    output = output

    return success, output, timed_out, truncated


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if urlparse(self.path).path != "/api/run":
            return _json_response(self, HTTPStatus.NOT_FOUND, {"success": False, "error": "Not found"})

        # Auth
        api_key = (os.environ.get("JATTI_API_KEY") or "").strip()
        if api_key:
            provided = (self.headers.get("X-API-Key") or "").strip()
            if provided != api_key:
                return _json_response(self, HTTPStatus.UNAUTHORIZED, {"success": False, "error": "Unauthorized"})

        # Read body with cap
        max_code_bytes = _get_env_int("JATTI_MAX_CODE_BYTES", 200_000)
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except Exception:
            length = 0

        if length <= 0 or length > max_code_bytes:
            return _json_response(
                self,
                HTTPStatus.REQUEST_ENTITY_TOO_LARGE if length > max_code_bytes else HTTPStatus.BAD_REQUEST,
                {"success": False, "error": "Code too large" if length > max_code_bytes else "Missing body"},
            )

        raw = self.rfile.read(length)
        try:
            body = json.loads(raw.decode("utf-8"))
        except Exception:
            body = {}

        code = body.get("code", "")
        if not isinstance(code, str) or not code.strip():
            return _json_response(self, HTTPStatus.BAD_REQUEST, {"success": False, "error": "Missing code"})

        success, output, timed_out, truncated = _run_jatti(code)

        return _json_response(
            self,
            HTTPStatus.OK,
            {"success": success, "output": output, "timedOut": timed_out, "truncated": truncated},
        )

    def do_GET(self):
        # Helpful for quick checks
        if urlparse(self.path).path == "/api/run":
            return _json_response(self, HTTPStatus.METHOD_NOT_ALLOWED, {"success": False, "error": "Use POST"})
        return _json_response(self, HTTPStatus.NOT_FOUND, {"success": False, "error": "Not found"})

    def log_message(self, format, *args):
        return
