FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml ./
RUN pip install --no-cache-dir celery redis fastapi structlog watchdog broadcaster uvicorn psycopg2-binary
COPY . .
