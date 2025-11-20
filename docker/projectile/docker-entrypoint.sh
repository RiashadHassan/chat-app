#!/bin/sh

#exit immediately if any command fails (non-zero exit code).
set -e

mkdir -p /app/projectile/mediafiles

# dockerfile bakes in static files
# this section is commented out to avoid redundant collection
# if [ "$RUN_COLLECTSTATIC" = "true" ]; then
#     echo "Collecting staticfiles..."
#     python manage.py collectstatic --noinput
# fi

if [ "$RUN_MIGRATIONS" = "true" ]; then
    echo "Running migrations..."
    python manage.py migrate --noinput
fi


if [ "$PRODUCTION" = "true" ]; then
    echo "Starting Uvicorn..."
    exec uvicorn projectile_settings.asgi:application \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --reload # only for development convenience, remove in real production

elif [ "$USE_DAPHNE" = "true" ]; then
    echo "Starting Daphne..."
    exec daphne -b 0.0.0.0 -p 8000 projectile_settings.asgi:application

else 
    # should never reach here in production
    echo "Starting Django Development Server..."
    exec python manage.py runserver 0.0.0.0:8000
    
fi
