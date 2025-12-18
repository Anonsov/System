FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# system deps (psycopg2 needs libpq)
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 10001 appuser \
  && mkdir -p /app/logs /app/media \
  && chown -R appuser:appuser /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Optional prod-only deps
COPY requirements-prod.txt /app/requirements-prod.txt
RUN pip install --no-cache-dir -r /app/requirements-prod.txt

COPY . /app

# Ensure perms after copy
RUN mkdir -p /app/logs /app/media \
  && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# overridden by docker-compose per service
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
