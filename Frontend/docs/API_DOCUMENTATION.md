# API Documentation — AI Assignment Generator

## Base URL

```
http://localhost:5000/api/v1
```

## Authentication

All protected endpoints require a JWT access token in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

### Authentication Flow

1. **Register** or **Login** to receive `access_token` and `refresh_token`
2. Include the `access_token` in every protected request
3. When the access token expires (HTTP 401), call the **Refresh** endpoint with your `refresh_token`
4. If the refresh token is expired, the user must log in again

---

## Endpoints

### 1. Auth — Register

| Field | Value |
|-------|-------|
| **Method** | `POST` |
| **URL** | `/api/v1/auth/register` |
| **Auth** | None |

**Request Body:**

```json
{
  "name": "Muzammal",
  "email": "muzammal@test.com",
  "password": "MyPass123"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | User display name |
| email | string | Yes | Valid email address |
| password | string | Yes | Min 6 characters |

**Response (201 Created):**

```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "name": "Muzammal",
      "email": "muzammal@test.com"
    },
    "access_token": "eyJ...",
    "refresh_token": "eyJ..."
  }
}
```

**cURL:**

```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Muzammal","email":"muzammal@test.com","password":"MyPass123"}'
```

---

### 2. Auth — Login

| Field | Value |
|-------|-------|
| **Method** | `POST` |
| **URL** | `/api/v1/auth/login` |
| **Auth** | None |

**Request Body:**

```json
{
  "email": "muzammal@test.com",
  "password": "MyPass123"
}
```

**Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "name": "Muzammal",
      "email": "muzammal@test.com"
    },
    "access_token": "eyJ...",
    "refresh_token": "eyJ..."
  }
}
```

**cURL:**

```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"muzammal@test.com","password":"MyPass123"}'
```

---

### 3. Auth — Refresh Token

| Field | Value |
|-------|-------|
| **Method** | `POST` |
| **URL** | `/api/v1/auth/refresh` |
| **Auth** | Bearer `<refresh_token>` |

**Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "access_token": "eyJ..."
  }
}
```

**cURL:**

```bash
curl -X POST http://localhost:5000/api/v1/auth/refresh \
  -H "Authorization: Bearer <refresh_token>"
```

---

### 4. Auth — Get Current User

| Field | Value |
|-------|-------|
| **Method** | `GET` |
| **URL** | `/api/v1/auth/me` |
| **Auth** | Bearer `<access_token>` |

**Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "Muzammal",
    "email": "muzammal@test.com"
  }
}
```

**cURL:**

```bash
curl http://localhost:5000/api/v1/auth/me \
  -H "Authorization: Bearer <access_token>"
```

---

### 5. Assignments — Generate

| Field | Value |
|-------|-------|
| **Method** | `POST` |
| **URL** | `/api/v1/assignments/generate` |
| **Auth** | Bearer `<access_token>` |

**Request Body:**

```json
{
  "topic": "Artificial Intelligence in Healthcare",
  "academic_level": "university",
  "word_count": 1500,
  "citation_style": "apa",
  "template": "professional"
}
```

| Field | Type | Required | Options |
|-------|------|----------|---------|
| topic | string | Yes | Free text |
| academic_level | string | Yes | `school`, `college`, `university`, `research` |
| word_count | integer | Yes | `800`, `1000`, `1200`, `1500`, `2000`, `3000`, `5000` |
| citation_style | string | Yes | `apa`, `mla`, `harvard`, `ieee` |
| template | string | Yes | `professional`, `academic`, `modern`, `minimal`, `colorful` |

**Response (202 Accepted):**

```json
{
  "success": true,
  "message": "Assignment generation started!",
  "data": {
    "assignment_id": "uuid",
    "status": "pending",
    "status_url": "/api/v1/assignments/uuid"
  }
}
```

**cURL:**

```bash
curl -X POST http://localhost:5000/api/v1/assignments/generate \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"topic":"AI in Healthcare","academic_level":"university","word_count":1500,"citation_style":"apa","template":"professional"}'
```

---

### 6. Assignments — List

| Field | Value |
|-------|-------|
| **Method** | `GET` |
| **URL** | `/api/v1/assignments` |
| **Auth** | Bearer `<access_token>` |

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| page | integer | 1 | Page number |
| per_page | integer | 10 | Items per page |
| status | string | — | Filter by status |

**Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "assignments": [
      {
        "id": "uuid",
        "topic": "AI in Healthcare",
        "academic_level": "university",
        "word_count": 1500,
        "status": "completed",
        "progress_percent": 100,
        "created_at": "2026-03-12T10:00:00Z",
        "completed_at": "2026-03-12T10:01:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 10,
      "total": 5,
      "total_pages": 1,
      "has_next": false,
      "has_prev": false
    }
  }
}
```

**cURL:**

```bash
curl "http://localhost:5000/api/v1/assignments?page=1&per_page=10" \
  -H "Authorization: Bearer <token>"
```

---

### 7. Assignments — Get Detail

| Field | Value |
|-------|-------|
| **Method** | `GET` |
| **URL** | `/api/v1/assignments/<id>` |
| **Auth** | Bearer `<access_token>` |

**Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "topic": "AI in Healthcare",
    "academic_level": "university",
    "word_count": 1500,
    "citation_style": "apa",
    "template": "professional",
    "status": "completed",
    "progress_percent": 100,
    "error_message": null,
    "created_at": "2026-03-12T10:00:00Z",
    "completed_at": "2026-03-12T10:01:00Z",
    "sections": [
      {
        "id": "uuid",
        "title": "Introduction",
        "content": "...",
        "order": 0,
        "image_prompt": ""
      }
    ],
    "images": [
      {
        "id": "uuid",
        "image_url": "/path/to/image.png",
        "caption": "Figure 1: ..."
      }
    ],
    "references": [
      {
        "id": "uuid",
        "citation": "Smith, J. (2025). AI in Healthcare...",
        "source_url": "https://...",
        "title": "AI in Healthcare"
      }
    ]
  }
}
```

**Assignment Status Flow:**

```
pending → researching → outlining → generating → imaging → formatting → completed
                                                                       → failed
```

**cURL:**

```bash
curl http://localhost:5000/api/v1/assignments/<id> \
  -H "Authorization: Bearer <token>"
```

---

### 8. Assignments — Download

| Field | Value |
|-------|-------|
| **Method** | `GET` |
| **URL** | `/api/v1/assignments/<id>/download` |
| **Auth** | Bearer `<access_token>` |

**Query Parameters:**

| Param | Type | Options | Description |
|-------|------|---------|-------------|
| format | string | `docx`, `pdf` | Document format |

**Response:** Binary file blob with appropriate content type.

**cURL:**

```bash
curl -O http://localhost:5000/api/v1/assignments/<id>/download?format=docx \
  -H "Authorization: Bearer <token>"
```

---

### 9. System — Health Check

| Field | Value |
|-------|-------|
| **Method** | `GET` |
| **URL** | `/api/v1/health` |
| **Auth** | None |

**Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "status": "healthy"
  }
}
```

**cURL:**

```bash
curl http://localhost:5000/api/v1/health
```

---

## Error Response Format

All errors follow this structure:

```json
{
  "success": false,
  "message": "Human-readable error description",
  "errors": {
    "field_name": ["Specific validation error"]
  }
}
```

### Common HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 202 | Accepted (async task started) |
| 400 | Bad Request (validation error) |
| 401 | Unauthorized (missing/invalid token) |
| 404 | Not Found |
| 422 | Unprocessable Entity |
| 500 | Internal Server Error |
