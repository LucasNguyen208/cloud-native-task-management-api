#!/bin/sh

echo "Waiting for MySQL..."

sleep 10

echo "Running database migrations..."

flask db upgrade

echo "Seeding roles..."

python seed.py

echo "Starting Gunicorn..."

exec gunicorn \
  --bind 0.0.0.0:5000 \
  --workers 4 \
  --timeout 60 \
  run:app
