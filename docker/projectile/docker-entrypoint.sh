#!/bin/sh

#exit immediately if any command fails (non-zero exit code).
set -e

echo "Collecting Staticfiles..."
python manage.py collectstatic --noinput

echo "Running Makemigrations..."
python manage.py makemigrations --noinput

echo "Running migrations..."
python manage.py migrate --noinput

if [ "$PRODUCTION" = "true" ]; then
    echo "Starting Uvicorn..."
    exec uvicorn projectile_settings.asgi:application --host 0.0.0.0 --port 8000 --workers 4

elif [ "$USE_DAPHNE" = "true" ]; then
    echo "Starting Daphne..."
    exec daphne -b 0.0.0.0 -p 8000 projectile_settings.asgi:application

else 
    echo "Starting Django Development Server..."
    exec python manage.py runserver 0.0.0.0:8000
    
fi
