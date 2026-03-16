#!/bin/bash
# =============================================================
# Celery Worker Startup Script
# =============================================================

set -e

echo "🚀 Starting Celery Worker..."
echo "   Broker: ${REDIS_URL:-redis://localhost:6379/0}"

celery -A app.tasks.assignment_tasks.celery worker \
    --loglevel=info \
    --concurrency=4 \
    --max-tasks-per-child=100 \
    --without-heartbeat \
    --without-gossip \
    --without-mingle \
    -Q default

echo "👋 Celery Worker stopped."