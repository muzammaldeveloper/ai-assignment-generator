# AI Assignment Generator Backend

A production-oriented Flask backend for generating structured academic assignments using LLM-powered writing, real-time web research, image generation, and export-ready document formatting.

## Overview

This service provides:

- Secure authentication with JWT access and refresh tokens.
- Assignment generation pipeline (research, outline, content, references, document export).
- Optional asynchronous processing with Celery + Redis.
- Multiple storage strategies (local filesystem or S3).
- Deployment support for local development and Docker-based environments.

## Core Capabilities

- AI text generation using Groq models.
- Live research enrichment via Tavily.
- Contextual image generation through Google Gemini.
- DOCX/PDF document generation pipeline.
- Input validation and prompt-guard protections.
- Rate limiting and structured error handling.

## Tech Stack

- Python 3.11+
- Flask, SQLAlchemy, Marshmallow
- JWT (flask-jwt-extended)
- Celery + Redis
- SQLite (default local) or PostgreSQL
- Docker and Docker Compose

## Project Layout

```text
Backend/
  app/
    api/            # HTTP endpoints
    models/         # SQLAlchemy models
    schemas/        # Request/response schemas
    services/       # Generation, research, and document services
    tasks/          # Celery task entry points
    utils/          # Validation, guards, logging, helpers
  config/           # Settings management
  tests/            # Pytest test suite
  docker-compose.yml
  Dockerfile
```

## Local Development Setup

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Update `.env` with valid API keys and runtime settings.

### 4. Run the API

```bash
flask run --host=0.0.0.0 --port=5000 --reload
```

### 5. Run worker (optional, separate terminal)

```bash
celery -A app.tasks.assignment_tasks.celery worker --loglevel=info --concurrency=4
```

## Environment Variables

Important variables (see `.env.example` for full list):

- `FLASK_APP`, `FLASK_ENV`, `DEBUG`
- `SECRET_KEY`, `JWT_SECRET_KEY`
- `DATABASE_URL` (SQLite or PostgreSQL)
- `REDIS_URL`
- `GROQ_API_KEY`, `GROQ_MODEL`
- `GEMINI_API_KEY`, `GEMINI_MODEL`
- `TAVILY_API_KEY`, `TAVILY_MAX_RESULTS`
- `STORAGE_BACKEND` (`local` or `s3`)

Notes:

- Application settings default to SQLite for local development.
- The provided `.env.example` includes a PostgreSQL sample URL for containerized deployments.

## Docker Setup

Start API, worker, PostgreSQL, and Redis:

```bash
docker-compose up --build -d
```

Stop and remove containers:

```bash
docker-compose down -v
```

## API Endpoints

Base path: `/api/v1`

| Method | Endpoint | Auth Required | Purpose |
| --- | --- | --- | --- |
| `GET` | `/health` | No | Service health check |
| `POST` | `/auth/register` | No | Register a new user |
| `POST` | `/auth/login` | No | Authenticate and issue tokens |
| `POST` | `/auth/refresh` | Refresh token | Rotate access token |
| `POST` | `/assignments/generate` | Access token | Generate an assignment |
| `GET` | `/assignments` | Access token | List user assignments |
| `GET` | `/assignments/<id>` | Access token | Get assignment details |
| `GET` | `/assignments/<id>/download` | Access token | Download generated file |

Example request:

```bash
curl -X POST http://localhost:5000/api/v1/assignments/generate \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Artificial Intelligence in Healthcare",
    "academic_level": "university",
    "word_count": 1500,
    "citation_style": "apa",
    "template": "professional"
  }'
```

## Quality and Testing

Run tests:

```bash
pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing
```

Run lint checks:

```bash
ruff check app/ tests/
ruff format --check app/ tests/
```

## Useful Make Targets

If using `make`, common commands include:

- `make run`
- `make worker`
- `make test`
- `make migrate`
- `make docker-up`
- `make docker-down`

## License

MIT