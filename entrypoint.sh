#!/bin/bash

# Wait for DB to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL is up."

# Run migrations
export FLASK_APP=app.py
flask db upgrade

# Start the app
exec python app.py
