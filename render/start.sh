#!/bin/sh
set -eu

# Render provides PORT. Default for local runs.
PORT="${PORT:-10000}"

# Make sure the Python server is only reachable locally.
APP_HOST="127.0.0.1"
APP_PORT="8000"

# Safety defaults (can be overridden by Render env vars)
: "${JATTI_TIMEOUT_SEC:=2.5}"
: "${JATTI_MAX_CODE_BYTES:=200000}"
: "${JATTI_MAX_OUTPUT_BYTES:=200000}"
: "${JATTI_RATE_WINDOW_SEC:=10}"
: "${JATTI_RATE_MAX_REQ:=30}"
: "${DEMO_COOKIE_MAX_AGE:=3600}"

if [ -z "${JATTI_API_KEY:-}" ]; then
  echo "JATTI_API_KEY is required for Render deployment" >&2
  exit 1
fi

python playground_server.py --host "$APP_HOST" --port "$APP_PORT" &

# Run Caddy in the foreground (Render expects one foreground process).
exec caddy run --config /etc/caddy/Caddyfile --adapter caddyfile
