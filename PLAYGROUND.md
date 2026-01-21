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
- `JATTI_API_KEY` (recommended)
- Optional limits: `JATTI_TIMEOUT_SEC`, `JATTI_MAX_CODE_BYTES`, `JATTI_MAX_OUTPUT_BYTES`

## Deploy (Render)

This repo includes a Render Blueprint at `render.yaml`.

It deploys a single Docker web service that runs:
- the Python playground server on `127.0.0.1:8000` (internal)
- an in-container reverse proxy on `$PORT` that:
  - injects `X-API-Key` for `/api/*`
  - uses the **Demo Mode** button (`/demo`) to enable running code

Steps:

1) In Render, create a new Blueprint and point it to your GitHub repo.
2) Render will create the service from `render.yaml`.
3) Deploy and open the `.onrender.com` URL.

Notes:
- Running code is enabled after clicking **Demo Mode**.
- You can tune limits with `JATTI_*` env vars in Render.

## Secure Deploy (Recommended)

For a more secure deployment, run the playground **behind a reverse proxy** that:
- Provides **demo mode** (no login) via a button that enables API access
- Supports optional **admin login** (HTTP Basic Auth) for API access
- Injects `X-API-Key` for `/api/*` requests so the browser **never needs to know** the API key
- Exposes only ports 80/443 publicly (the app container is not published)

This repo includes:
- `docker-compose.secure.yml`
- `Caddyfile`

### 1) Create `.env`

Copy `.env.example` → `.env` and set at minimum:

- `JATTI_API_KEY` (a long random string)
- `SITE_ADDRESS` (your domain, e.g. `playground.example.com`)
- `BASIC_AUTH_USER`
- `BASIC_AUTH_HASH`

### 2) Generate `BASIC_AUTH_HASH`

On the server with Docker installed:

- `docker run --rm caddy:2 caddy hash-password --plaintext "yourPasswordHere"`

Put the output hash into `.env` as `BASIC_AUTH_HASH=...`.

### 3) Start

- `docker compose -f docker-compose.secure.yml up --build -d`

Open:
- `https://<your-domain>/`

Notes:
- Caddy will automatically provision TLS certificates for real domains.
- For local testing, set `SITE_ADDRESS=:80` and use `http://localhost/`.

### Demo Mode (no login)

With the secure proxy setup:
- The UI loads without credentials.
- Clicking **Demo Mode** sets a short-lived cookie and enables running code.
- Use **Exit Demo** to disable it.

You can control demo cookie lifetime with:
- `DEMO_COOKIE_MAX_AGE` (default 3600 seconds)

## Hardening (Important)

If you bind the server to `0.0.0.0` or deploy on a VPS, set an API key and limits.

### API Key

- Set env var: `JATTI_API_KEY`
- The UI uses the API without a key by default. For public deployments, put the playground behind a reverse proxy that injects the header or protect the whole site with auth.

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
- Edit values (especially `JATTI_API_KEY`)

### Public bind

- `python playground_server.py --host 0.0.0.0 --port 8000`

Warning: even with these limits, this is not a full sandbox.

## Configuration

- Change port/host:
  - `python playground_server.py --port 9000`
  - `python playground_server.py --host 127.0.0.1 --port 8000`
