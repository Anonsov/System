#!/usr/bin/env sh
set -eu

mkdir -p /app/logs /app/media

python manage.py migrate

# Idempotent imports (safe to re-run)
python manage.py import_abramyan_series
python manage.py import_abramyan_for
python manage.py import_abramyan_while

exec python manage.py runserver 0.0.0.0:8000
