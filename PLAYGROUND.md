# Jatti Playground (Web Frontend)

This repo includes a simple local web UI with **two panes**:
- Left: Jatti code editor
- Right: output

It runs code locally via a small Python HTTP server.

## Run (Windows)

From the repo root:

- `python playground_server.py`

Then open:
- `http://127.0.0.1:8000/`

## Notes

- This executes code on your machine. Keep it on localhost.
- If you use a virtualenv, run with that Python (e.g. `.venv/Scripts/python.exe playground_server.py`).
- Shortcut: **Ctrl+Enter** to run.

## Deploy (Docker)

Only recommended for private demos (LAN/VPN) unless you add proper sandboxing.

- Build:
  - `docker build -t jatti-playground .`
- Run:
  - `docker run --rm -p 8000:8000 jatti-playground`
- Open:
  - `http://localhost:8000/`

## Deploy (Vercel)

This repo is Vercel-ready:
- UI: served from `frontend/` via `vercel.json` rewrites
- API: `api/run.py` at `/api/run`

In Vercel Project Settings → Environment Variables, set:
- Optional: `JATTI_REQUIRE_API_KEY=1` and `JATTI_API_KEY` (to enforce X-API-Key)
- Optional limits: `JATTI_TIMEOUT_SEC`, `JATTI_MAX_CODE_BYTES`, `JATTI_MAX_OUTPUT_BYTES`

## Deploy (Render)

This repo includes a Render Blueprint at `render.yaml`.

It deploys a single Docker web service that runs:
- the Python playground server on `127.0.0.1:8000` (internal)
- an in-container reverse proxy on `$PORT` that:
  - injects `X-API-Key` for `/api/*`
  - keeps the API key out of the browser (recommended)

Steps:

1) In Render, create a new Blueprint and point it to your GitHub repo.
2) Render will create the service from `render.yaml`.
3) Deploy and open the `.onrender.com` URL.

Notes:
- If you enable auth (`JATTI_REQUIRE_API_KEY=1`), the proxy can inject `X-API-Key` for `/api/*` so the browser doesn't need to know the key.
- You can tune limits with `JATTI_*` env vars in Render.

## Secure Deploy (Recommended)

For a deployment, run the playground **behind a reverse proxy** that:
- Injects `X-API-Key` for `/api/*` requests so the browser **never needs to know** the API key
- Exposes only ports 80/443 publicly (the app container is not published)

This repo includes:
- `docker-compose.secure.yml`
- `Caddyfile`

### 1) Create `.env`

Copy `.env.example` → `.env` and set at minimum:

- Optional (if enabling auth): `JATTI_REQUIRE_API_KEY=1` and `JATTI_API_KEY` (a long random string)
- `SITE_ADDRESS` (your domain, e.g. `playground.example.com`)

### 2) Start

- `docker compose -f docker-compose.secure.yml up --build -d`

Open:
- `https://<your-domain>/`

Notes:
- Caddy will automatically provision TLS certificates for real domains.
- For local testing, set `SITE_ADDRESS=:80` and use `http://localhost/`.

## Hardening (Important)

If you bind the server to `0.0.0.0` or deploy on a VPS, set an API key and limits.

### API Key

- Optional: set `JATTI_REQUIRE_API_KEY=1` and `JATTI_API_KEY`
- The UI can send `X-API-Key` directly (API Key box), or you can keep the key out of the browser by using a reverse proxy that injects the header.

Tip: you can also create a `.env` file in the repo root (see `.env.example`). The server will load it automatically.

### Limits (env vars)

- `JATTI_TIMEOUT_SEC` (default `2.5`)
- `JATTI_MAX_CODE_BYTES` (default `200000`)
- `JATTI_MAX_OUTPUT_BYTES` (default `200000`)
- `JATTI_RATE_WINDOW_SEC` (default `10`)
- `JATTI_RATE_MAX_REQ` (default `30` per window per IP)

### .env file

Create `.env` from `.env.example`:

- Copy: `.env.example` → `.env`
- Edit values (especially `JATTI_REQUIRE_API_KEY` / `JATTI_API_KEY` if enabling auth)

### Public bind

- `python playground_server.py --host 0.0.0.0 --port 8000`

Warning: even with these limits, this is not a full sandbox.

## Configuration

- Change port/host:
  - `python playground_server.py --port 9000`
  - `python playground_server.py --host 127.0.0.1 --port 8000`
