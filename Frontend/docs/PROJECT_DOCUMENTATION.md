# Project Documentation — AI Assignment Generator

## 1. Project Overview

The **AI Assignment Generator** is a full-stack web application that uses artificial intelligence to generate professional academic assignments. Users can input a topic and configure parameters (academic level, word count, citation style, template), and the system produces a fully structured, research-backed document with AI-generated images, available for download as DOCX or PDF.

---

## 2. System Architecture

```
┌──────────────┐         ┌──────────────────┐         ┌──────────────────┐
│   Frontend   │ ──API──▶│   Flask Backend   │ ──────▶│   AI Services    │
│   (Next.js)  │◀────── │   (REST API)      │◀────── │  GPT-4o, Gemini  │
└──────────────┘         └──────────────────┘         └──────────────────┘
                                │                            │
                         ┌──────▼──────┐              ┌──────▼──────┐
                         │  PostgreSQL  │              │  Web Search │
                         │  Database    │              │  (Tavily)   │
                         └─────────────┘              └─────────────┘
```

- **Frontend**: Next.js 15 (App Router) served on port 3000, proxies API calls to backend
- **Backend**: Flask REST API on port 5000 with Celery for async task processing
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI Pipeline**: GPT-4o (content), Gemini (images), Tavily (web research)
- **Task Queue**: Celery with Redis broker for background assignment generation

---

## 3. Tech Stack

### Frontend
| Technology | Purpose |
|-----------|---------|
| Next.js 15 | React framework with App Router |
| Tailwind CSS | Utility-first CSS with custom dark theme |
| Framer Motion | Page transitions and micro-animations |
| Axios | HTTP client with interceptors for auth |
| js-cookie | JWT token storage |
| Lucide React | Icon library |
| React Hot Toast | Toast notifications |

### Backend
| Technology | Purpose |
|-----------|---------|
| Flask | Python web framework |
| SQLAlchemy | ORM for database models |
| Flask-JWT-Extended | JWT authentication |
| Celery | Async task processing |
| Redis | Message broker for Celery |
| PostgreSQL | Relational database |
| Gunicorn | WSGI production server |

### AI Services
| Service | Purpose |
|---------|---------|
| OpenAI GPT-4o | Content generation, outline creation |
| Google Gemini | AI image generation |
| Tavily API | Real-time web research |

---

## 4. Folder Structure

### Frontend (`frontend/`)

```
frontend/
├── package.json             # Dependencies and scripts
├── next.config.js           # Next.js config with API proxy
├── tailwind.config.js       # Tailwind theme customization
├── postcss.config.js        # PostCSS plugins
├── .env.local               # Environment variables
├── jsconfig.json            # Path aliases
├── public/
│   └── favicon.ico
└── src/
    ├── app/                 # Next.js App Router pages
    │   ├── layout.js        # Root layout with Toaster
    │   ├── page.js          # Landing page
    │   ├── globals.css      # Global styles + Tailwind
    │   ├── login/page.js    # Login page
    │   ├── register/page.js # Register page
    │   ├── dashboard/
    │   │   ├── layout.js    # Protected dashboard layout
    │   │   ├── page.js      # Assignment list
    │   │   └── [id]/page.js # Assignment detail
    │   ├── generate/page.js # Multi-step wizard
    │   └── docs/page.js     # API documentation
    ├── components/          # Reusable UI components
    ├── lib/                 # API client, auth helpers, constants
    └── hooks/               # Custom React hooks
```

### Backend (`app/`)

```
app/
├── api/                 # Route handlers
├── models/              # SQLAlchemy models
├── schemas/             # Marshmallow serialization schemas
├── services/            # Business logic (AI pipeline, document generation)
├── tasks/               # Celery background tasks
├── templates/           # Document templates
├── utils/               # Helpers, validators, logger
├── errors/              # Error handlers
└── extensions.py        # Flask extension instances
```

---

## 5. Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL
- Redis

### Backend Setup

```bash
# Clone the repository
git clone <repo-url>
cd ai-assignment-generator

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database, API keys, etc.

# Initialize database
flask db upgrade

# Seed demo data
python scripts/seed_db.py

# Start the Flask server
flask run

# In a separate terminal, start Celery worker
celery -A app.tasks worker --loglevel=info
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend runs on `http://localhost:3000` and proxies API calls to `http://localhost:5000`.

---

## 6. Environment Variables

### Backend (`.env`)

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost/dbname` |
| `SECRET_KEY` | Flask secret key | Random string |
| `JWT_SECRET_KEY` | JWT signing key | Random string |
| `OPENAI_API_KEY` | OpenAI API key for GPT-4o | `sk-...` |
| `GOOGLE_API_KEY` | Google API key for Gemini | `AI...` |
| `TAVILY_API_KEY` | Tavily API key for web search | `tvly-...` |
| `REDIS_URL` | Redis broker URL | `redis://localhost:6379/0` |

### Frontend (`.env.local`)

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `http://localhost:5000/api/v1` |

---

## 7. API Endpoints Summary

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/v1/auth/register` | No | Register new user |
| POST | `/api/v1/auth/login` | No | Login |
| POST | `/api/v1/auth/refresh` | Yes | Refresh access token |
| GET | `/api/v1/auth/me` | Yes | Get user profile |
| POST | `/api/v1/assignments/generate` | Yes | Start assignment generation |
| GET | `/api/v1/assignments` | Yes | List assignments |
| GET | `/api/v1/assignments/:id` | Yes | Get assignment detail |
| GET | `/api/v1/assignments/:id/download` | Yes | Download DOCX/PDF |
| GET | `/api/v1/health` | No | Health check |

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for full details.

---

## 8. Database Schema

### Users Table
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| name | VARCHAR | User display name |
| email | VARCHAR | Unique email |
| password_hash | VARCHAR | Bcrypt hashed password |
| created_at | TIMESTAMP | Account creation time |

### Assignments Table
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | UUID | Foreign key → users |
| topic | TEXT | Assignment topic |
| academic_level | VARCHAR | school/college/university/research |
| word_count | INTEGER | Target word count |
| citation_style | VARCHAR | apa/mla/harvard/ieee |
| template | VARCHAR | Document template name |
| status | VARCHAR | Current processing status |
| progress_percent | INTEGER | 0-100 completion percentage |
| error_message | TEXT | Error details if failed |
| created_at | TIMESTAMP | Creation time |
| completed_at | TIMESTAMP | Completion time |

### Sections Table
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| assignment_id | UUID | Foreign key → assignments |
| title | VARCHAR | Section heading |
| content | TEXT | Section body text |
| order | INTEGER | Display order |
| image_prompt | TEXT | Prompt used for image generation |

### Images Table
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| assignment_id | UUID | Foreign key → assignments |
| image_url | VARCHAR | Path to stored image |
| caption | VARCHAR | Image caption |

### References Table
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| assignment_id | UUID | Foreign key → assignments |
| citation | TEXT | Formatted citation string |
| source_url | VARCHAR | Original source URL |
| title | VARCHAR | Source title |

---

## 9. AI Pipeline Flow

The assignment generation pipeline runs as a Celery background task:

```
1. PENDING       → Task queued
2. RESEARCHING   → Tavily web search for topic research
3. OUTLINING     → GPT-4o creates section outline
4. GENERATING    → GPT-4o generates content for each section
5. IMAGING       → Gemini generates relevant images
6. FORMATTING    → Document assembled into DOCX/PDF
7. COMPLETED     → Assignment ready for download
   or FAILED     → Error captured and stored
```

Each step updates the assignment's `status` and `progress_percent` in real-time, which the frontend polls every 5 seconds.

---

## 10. Security Features

- **JWT Authentication**: Access tokens (short-lived) + refresh tokens (long-lived)
- **Password Hashing**: Bcrypt with salt
- **Input Validation**: Marshmallow schemas validate all request data
- **Prompt Guard**: Content filtering to prevent prompt injection
- **CORS**: Configured to allow only trusted origins
- **Rate Limiting**: API rate limiting per user
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries

---

## 11. Deployment Guide

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build -d
```

The `docker-compose.yml` includes:
- Flask app (Gunicorn)
- Celery worker
- PostgreSQL
- Redis

### Manual Deployment

1. Set up PostgreSQL and Redis on the server
2. Configure environment variables
3. Run database migrations: `flask db upgrade`
4. Start backend: `gunicorn -c gunicorn.conf.py "app.factory:create_app()"`
5. Start Celery: `celery -A app.tasks worker --loglevel=info`
6. Build frontend: `cd frontend && npm run build`
7. Start frontend: `npm start`

---

## 12. Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend won't start | Check `.env` file, ensure PostgreSQL and Redis are running |
| JWT errors | Ensure `JWT_SECRET_KEY` is set, tokens aren't expired |
| Assignment stuck in "pending" | Check Celery worker is running, check Redis connection |
| Frontend can't reach API | Verify `next.config.js` proxy and backend is on port 5000 |
| Database errors | Run `flask db upgrade` to apply latest migrations |
| AI generation fails | Check API keys (OpenAI, Google, Tavily) in `.env` |
| CORS errors | Ensure backend CORS config allows `http://localhost:3000` |
