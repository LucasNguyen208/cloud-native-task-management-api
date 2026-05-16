#!/bin/sh

echo "Waiting for MySQL..."

sleep 10

echo "Running database migrations..."

flask db upgrade

echo "Seeding roles..."

python seed.py

echo "Starting Flask app..."

python run.py
