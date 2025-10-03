#!/bin/bash
set -e

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Seed the database (if you have a seeding script)
# Uncomment and modify the following line if you have a seeding script
echo "Seeding database..."
python bytebox/config/seeder.py

# Start the application
echo "Starting uvicorn server..."
exec uvicorn bytebox.main:app --host 0.0.0.0 --port 8000 --reload
