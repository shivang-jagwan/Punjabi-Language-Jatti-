# Deployment (Docker / Vercel / Render)

Security warning: this project executes user-provided code. Deploying publicly without sandboxing is risky.

## Environment variables

- `JATTI_REQUIRE_API_KEY` (default `0`): when set to `1`, `/api/run` requires `X-API-Key`.
- `JATTI_API_KEY`: API key value (only used if `JATTI_REQUIRE_API_KEY=1`).
- Limits:
  - `JATTI_TIMEOUT_SEC` (default `2.5`)
  - `JATTI_MAX_CODE_BYTES` (default `200000`)
  - `JATTI_MAX_OUTPUT_BYTES` (default `200000`)
  - `JATTI_RATE_WINDOW_SEC` (default `10`)
  - `JATTI_RATE_MAX_REQ` (default `30`)

## Docker (simple)

```bash
docker build -t jatti-playground .
docker run --rm -p 8000:8000 jatti-playground
```

Open `http://localhost:8000/`.

## Vercel

This repo includes:
- UI: `frontend/`
- API: `api/run.py` (`/api/run`) and `api/healthz.py` (`/api/healthz`)
- Routing: `vercel.json`

In Vercel → Project → Settings → Environment Variables:
- Leave auth disabled (your request):
  - Do NOT set `JATTI_REQUIRE_API_KEY`, or set it to `0`

(Optional) Enable auth later:
- Set `JATTI_REQUIRE_API_KEY=1`
- Set a strong `JATTI_API_KEY`

## Render (Docker Web Service)

If you can’t use Blueprint, create a **Web Service** manually:

- Runtime: Docker
- Dockerfile path: `render/Dockerfile`

Environment variables:
- To keep it open (your request): `JATTI_REQUIRE_API_KEY=0`
- Optional limits as needed

Render will provide a public URL like `https://<service>.onrender.com`.

## Reverse proxy header injection (optional)

If you enable auth but don’t want the browser to know the key, run behind a reverse proxy that injects `X-API-Key` for `/api/*`.

This repo includes:
- `docker-compose.secure.yml`
- `Caddyfile`

(Enable auth) set in `.env`:
- `JATTI_REQUIRE_API_KEY=1`
- `JATTI_API_KEY=<random>`
- `SITE_ADDRESS=<your-domain>`
