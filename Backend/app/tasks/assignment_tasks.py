"""
Celery Tasks — Optional for local.

Local mode uses threading instead (see assignment_api.py).
This file exists for production deployment with Redis.
"""

from __future__ import annotations

try:
    from celery import Celery
    from config.settings import get_settings

    settings = get_settings()

    celery = Celery(
        "ai_assignment_generator",
        broker=settings.redis_url,
        backend=settings.redis_url,
    )

    celery.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
        task_track_started=True,
        task_soft_time_limit=300,
        task_time_limit=360,
    )

    @celery.task(bind=True, name="generate_assignment", max_retries=2)
    def generate_assignment_task(self, assignment_id: str) -> dict:
        """Celery task for production (Redis required)."""
        from app.factory import create_app
        from app.services.pipeline_service import PipelineService

        app = create_app()
        with app.app_context():
            try:
                pipeline = PipelineService(settings=settings)
                pipeline.execute(assignment_id=assignment_id)
                return {"assignment_id": assignment_id, "status": "completed"}
            except Exception as exc:
                if self.request.retries < self.max_retries:
                    raise self.retry(exc=exc)
                return {"assignment_id": assignment_id, "status": "failed", "error": str(exc)}

except ImportError:
    # Celery not installed — local mode only
    pass