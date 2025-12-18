#!/usr/bin/env sh
set -eu

mkdir -p /app/logs /app/media

python manage.py migrate

# optional one-time imports on boot (disable by setting RUN_IMPORTS=0)
if [ "${RUN_IMPORTS:-1}" = "1" ]; then
  python manage.py import_abramyan_series
  python manage.py import_abramyan_for
  python manage.py import_abramyan_while
fi

# static assets (optional)
if [ "${COLLECTSTATIC:-0}" = "1" ]; then
  python manage.py collectstatic --noinput
fi

exec gunicorn system.wsgi:application --bind 0.0.0.0:8000 --workers ${GUNICORN_WORKERS:-3} --timeout ${GUNICORN_TIMEOUT:-120}
