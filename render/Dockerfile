FROM caddy:2 AS caddybin

FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY --from=caddybin /usr/bin/caddy /usr/bin/caddy

# App code
COPY . /app

# Render reverse proxy config
COPY render/Caddyfile /etc/caddy/Caddyfile
COPY render/start.sh /start.sh
RUN chmod +x /start.sh

# Run as non-root
RUN adduser --disabled-password --gecos "" appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 10000

CMD ["/start.sh"]
