#!/bin/sh

set -e

# now safe to call manage.py
exec "$@"

echo "Collecting Staticfiles..."
python manage.py collectstatic --noinput

echo "Running Makemigrations..."
python manage.py makemigrations --noinput

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting Uvicorn..."
exec uvicorn projectile_settings.asgi:application --host 0.0.0.0 --port 8000 --workers 4


# exec python manage.py runserver 0.0.0.0:8000
# exec daphne -b 0.0.0.0 -p 8000 projectile_settings.asgi:application