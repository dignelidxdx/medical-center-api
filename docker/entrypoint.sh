#!/bin/sh
set -e
echo "Waiting for PostgreSQL at ${POSTGRES_HOST:-db}:${POSTGRES_PORT:-5432}..."
until nc -z "${POSTGRES_HOST:-db}" "${POSTGRES_PORT:-5432}"; do
  sleep 1
done
echo "PostgreSQL is available. Applying migrations..."
python manage.py migrate --noinput
exec "$@"

