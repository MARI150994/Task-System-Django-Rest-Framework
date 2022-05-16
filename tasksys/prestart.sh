#!/bin/sh

set -e
echo "Apply migrations"
python manage.py migrate
echo "migrations ok"

exec "$@"