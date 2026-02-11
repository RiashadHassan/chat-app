#!/bin/bash
set -e

echo "========================================"
echo "Full App Development Setup With Microservices"
echo "========================================"
echo ""

# Set environment variables
export POSTGRES_USER=chat_app_user
export POSTGRES_DB=chat_app_db

echo "ENV vars set:"
echo "POSTGRES_USER=$POSTGRES_USER"
echo "POSTGRES_DB=$POSTGRES_DB"
echo ""

# Ensure PgBouncer auth file exists BEFORE docker up
echo "Preparing PgBouncer auth file..."
mkdir -p ../db/pgbouncer
touch ../db/pgbouncer/userlist.txt
echo ""

# Build Docker images
echo "Building Docker images with no-cache (fresh build)..."
docker compose -f docker-compose.db.yml -f docker-compose.django.yml -f docker-compose.infra.yml up -d
echo ""

# Start services
echo "Starting services..."
# docker compose up -d
echo ""

# Wait for database to be ready
echo "Waiting for PostgreSQL to be ready..."
until docker compose -f docker-compose.db.yml exec db pg_isready -U "$POSTGRES_USER" > /dev/null 2>&1; do
    echo "Postgres is not ready yet... retrying in 2s"
    sleep 2
done
echo "PostgreSQL is ready!"
echo ""

# Generate userlist.txt
echo "Generating PgBouncer userlist.txt..."
docker compose -f docker-compose.db.yml exec db psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Atc \
"SELECT '\"' || rolname || '\" \"' || rolpassword || '\"'
 FROM pg_authid
 WHERE rolcanlogin;" > ../db/pgbouncer/userlist.txt

echo "userlist.txt updated with auth credentials!"
echo ""

# Restart PgBouncer to reload auth
echo "Restarting PgBouncer..."
docker compose -f docker-compose.db.yml restart pgbouncer
echo ""

echo "========================================"
echo "Development Setup Complete"
echo "========================================"
