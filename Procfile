web: gunicorn system.wsgi:application --log-file -
worker: celery -A system worker -l info -Q judge --concurrency=1 --prefetch-multiplier=1
release: python manage.py migrate
