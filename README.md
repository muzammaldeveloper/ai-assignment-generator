# AI Assignment Generator

AI Assignment Generator is a full-stack application that helps users generate structured academic assignments using AI text generation, web research, and document export features.

It includes:

- A Flask backend API with authentication, assignment pipeline, and document generation.
- A Next.js frontend for user authentication, assignment creation, and dashboard access.

## Repository Structure

```text
ai-assignment-generator/
  Backend/    # Flask API, Celery worker, models, tests
  Frontend/   # Next.js app (App Router)
```

## Key Features

- JWT-based authentication (access + refresh flow)
- AI writing pipeline for academic assignment generation
- Research enrichment using Tavily
- Image generation integration via Gemini
- DOCX/PDF document support
- Async background processing with Celery + Redis
- Responsive frontend built with Next.js and Tailwind CSS

## Tech Stack

Backend:

- Python 3.11+
- Flask, SQLAlchemy, Marshmallow
- Celery + Redis
- SQLite (local default) or PostgreSQL

Frontend:

- Next.js 15
- React 19
- Tailwind CSS
- Axios

## Quick Start (Local)

### 1. Backend setup

```bash
cd Backend
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

Install dependencies:

```bash
pip install -r requirements.txt
```

Create environment file:

```bash
cp .env.example .env
```

Run backend API:

```bash
flask run --host=0.0.0.0 --port=5000 --reload
```

Optional: run worker in a new terminal:

```bash
celery -A app.tasks.assignment_tasks.celery worker --loglevel=info --concurrency=4
```

### 2. Frontend setup

```bash
cd Frontend
npm install
npm run dev
```

Frontend default URL: http://localhost:3000

Backend default URL: http://localhost:5000

## Docker (Backend)

From Backend folder:

```bash
docker-compose up --build -d
```

Stop services:

```bash
docker-compose down -v
```

## API Base Path

All backend endpoints are served under:

```text
/api/v1
```

Main endpoint groups:

- `/health`
- `/auth/*`
- `/assignments/*`

## Testing

Backend tests:

```bash
cd Backend
pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing
```

Frontend lint:

```bash
cd Frontend
npm run lint
```

## GitHub Push Checklist

- Ensure `.env` files are not committed.
- Ensure virtual environments and build artifacts are ignored.
- Run backend tests successfully.
- Run frontend lint and production build.
- Confirm README and project structure are up to date.

## License

MIT