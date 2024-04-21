#!/bin/bash
echo "Create migrations"
alembic revision --autogenerate
echo "============================="

echo "Migrate"
alembic upgrade head
echo "============================="

echo "Start server"
uvicorn api.main:app --reload --port=8000 --host=0.0.0.0