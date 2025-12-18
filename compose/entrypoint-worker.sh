#!/usr/bin/env sh
set -eu

# Start Celery worker for judge queue
exec celery -A system worker -l info -Q judge --concurrency=1 --prefetch-multiplier=1
