# Backend API

Base path: /api/v1

## Auth

- POST /auth/register
- POST /auth/login
- POST /auth/refresh

## Assignments

- POST /assignments/generate
- GET /assignments
- GET /assignments/{id}
- GET /assignments/{id}/download

## Health

- GET /health

## API Standards

- Consistent success/error envelope
- Request validation with clear field-level errors
- Request ID attached to responses
