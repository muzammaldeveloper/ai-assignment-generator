# Architecture

## High-Level Components

- Next.js frontend
- Flask API
- Celery worker
- Redis broker
- SQL database
- AI providers: Groq, Tavily, Gemini

## Data Flow

1. User submits generation request from frontend.
2. API validates input and enqueues pipeline work.
3. Worker executes research, outline, draft, imaging, export stages.
4. API serves assignment status and downloadable artifacts.

## Scalability Notes

- Separate queue types for heavy and light tasks.
- Add object storage with signed URLs for generated files.
- Add metrics and tracing for request and task correlation.
