FROM python:3.11-slim AS base

# Prevent Python from buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# ── System Dependencies ──
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ── Python Dependencies (cached layer) ──
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# ── Application Code ──
COPY . .

# ── Create storage directories ──
RUN mkdir -p storage/images storage/documents

# ── Non-root user for security ──
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

CMD ["gunicorn", "app.factory:create_app()", "--config", "gunicorn.conf.py"]