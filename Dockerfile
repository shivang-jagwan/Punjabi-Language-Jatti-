# Jatti Playground Docker image
# NOTE: This runs user-provided code. Do NOT expose publicly without sandboxing/auth.

FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1

# No external deps required (stdlib only)
COPY . /app

RUN adduser --disabled-password --gecos "" appuser \
	&& chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["python", "playground_server.py", "--host", "0.0.0.0", "--port", "8000"]
