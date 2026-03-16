# AI Assignment Generator

AI Assignment Generator is a full-stack platform that generates professional academic assignments using AI writing, real-time web research, citation-aware structure, and export-ready documents.

## Highlights

- End-to-end assignment generation pipeline
- JWT authentication with refresh-token flow
- Research integration through Tavily
- AI text generation through Groq
- Image generation through Google Gemini
- DOCX and PDF document export
- Celery background processing with Redis
- Modern Next.js frontend dashboard

## System Architecture

```text
Frontend (Next.js)
  |
  v
Backend API (Flask)
  |
  +--> Auth + Validation + Rate Limiting
  +--> Assignment Pipeline (Research -> Outline -> Writing -> Export)
  +--> Async Jobs (Celery + Redis)
  |
  +--> External Services
    - Groq (text)
    - Tavily (research)
    - Gemini (images)
```

## Repository Structure

```text
ai-assignment-generator/
├── Backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── tasks/
│   │   ├── templates/
│   │   └── utils/
│   ├── config/
│   ├── migrations/
│   ├── scripts/
│   ├── tests/
│   ├── docker-compose.yml
│   └── requirements.txt
├── Frontend/
│   ├── src/app/
│   ├── src/components/
│   ├── src/hooks/
│   ├── src/lib/
│   └── package.json
└── README.md
```

## Backend API Reference

Base URL: `/api/v1`

| Method | Endpoint | Auth | Description |
| --- | --- | --- | --- |
| GET | /health | No | Health status endpoint |
| POST | /auth/register | No | Register a new user |
| POST | /auth/login | No | Login and get tokens |
| POST | /auth/refresh | Refresh Token | Issue a new access token |
| POST | /assignments/generate | Access Token | Start assignment generation |
| GET | /assignments | Access Token | Get user assignments list |
| GET | /assignments/{id} | Access Token | Get assignment details |
| GET | /assignments/{id}/download | Access Token | Download generated file |

## Frontend Screenshots

### Home, Auth, and Generation Flow

| Screen 1 | Screen 2 |
| --- | --- |
| ![Frontend Screenshot 1](img/1.png) | ![Frontend Screenshot 2](img/2.png) |
| ![Frontend Screenshot 3](img/3.png) | ![Frontend Screenshot 4](img/4.png) |
| ![Frontend Screenshot 5](img/5.png) | ![Frontend Screenshot 6](img/6.png) |

### Dashboard and Assignment Views

| Screen 7 | Screen 8 |
| --- | --- |
| ![Frontend Screenshot 7](img/7.png) | ![Frontend Screenshot 8](img/8.png) |
| ![Frontend Screenshot 9](img/9.png) | ![Frontend Screenshot 10](img/10.png) |
| ![Frontend Screenshot 11](img/11.png) | |

## Quick Start

### Backend

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

Install and run:

```bash
pip install -r requirements.txt
cp .env.example .env
flask run --host=0.0.0.0 --port=5000 --reload
```

Optional worker:

```bash
celery -A app.tasks.assignment_tasks.celery worker --loglevel=info --concurrency=4
```

### Frontend

```bash
cd Frontend
npm install
npm run dev
```

Local URLs:

- Frontend: http://localhost:3000
- Backend: http://localhost:5000

## Docker (Backend)

```bash
cd Backend
docker-compose up --build -d
docker-compose down -v
```

## Quality Checks

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

## License

MIT