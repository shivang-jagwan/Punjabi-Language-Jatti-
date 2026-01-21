from __future__ import annotations

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"{\"ok\":true}")

    def log_message(self, format, *args):
        return
