#!/bin/bash
echo "Starting Flask App..."

export FLASK_APP=app.py
flask db upgrade

exec python app.py