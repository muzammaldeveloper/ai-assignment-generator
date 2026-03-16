.PHONY: run worker test lint migrate seed clean docker-up docker-down

# ── Development ──
run:
	flask run --host=0.0.0.0 --port=5000 --reload

worker:
	celery -A app.tasks.assignment_tasks.celery worker --loglevel=info --concurrency=4

# ── Testing ──
test:
	pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing

test-fast:
	pytest tests/ -x -v --tb=short

# ── Code Quality ──
lint:
	ruff check app/ tests/
	ruff format --check app/ tests/

format:
	ruff format app/ tests/

# ── Database ──
migrate:
	flask db migrate -m "Auto migration"
	flask db upgrade

seed:
	python scripts/seed_db.py

db-reset:
	flask db downgrade base
	flask db upgrade

# ── Docker ──
docker-up:
	docker-compose up --build -d

docker-down:
	docker-compose down -v

docker-logs:
	docker-compose logs -f

# ── Cleanup ──
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf storage/images/* storage/documents/*
	rm -rf htmlcov/ .coverage .pytest_cache