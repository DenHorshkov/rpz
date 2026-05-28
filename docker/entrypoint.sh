#!/usr/bin/env bash
set -e

if [ "${RUN_MIGRATIONS:-1}" = "1" ]; then
    echo ">>> Applying migrations…"
    python manage.py migrate --noinput
fi

if [ "${RUN_COLLECTSTATIC:-1}" = "1" ]; then
    echo ">>> Collecting static files…"
    python manage.py collectstatic --noinput
fi

exec "$@"
