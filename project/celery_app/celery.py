"""
This module configures the Celery application with Redis broker/backend
and sets up task routing and concurrency controls following Celery 5.5.3 best practices.
"""

# Load environment variables FIRST, before any other imports
from celery import Celery
import os


class Config:
    """Celery configuration following 5.5.3 best practices."""

    broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
    result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

    # Worker configuration for concurrency control
    worker_concurrency = int(os.environ.get("CELERY_WORKER_CONCURRENCY", "2"))
    worker_prefetch_multiplier = 1  # Only take 1 task at a time per worker
    worker_disable_rate_limits = True  # Allow unlimited queuing

    # Task configuration
    task_acks_late = True  # Only acknowledge after task completion
    task_reject_on_worker_lost = True  # Reject tasks if worker dies
    task_serializer = "json"
    accept_content = ["json"]
    result_serializer = "json"
    timezone = "UTC"
    enable_utc = True

    # Result backend configuration
    result_expires = 3600  # Results expire after 1 hour

    # Task execution configuration
    task_always_eager = False  # Don't execute tasks synchronously in development
    task_eager_propagates = True

    # Monitoring and logging
    worker_log_format = "[%(asctime)s: %(levelname)s/%(processName)s] %(message)s"
    worker_task_log_format = "[%(asctime)s: %(levelname)s/%(processName)s] [%(task_name)s(%(task_id)s)] %(message)s"

    # Task routing configuration
    task_routes = {
        "create_task": {
            "queue": "celery_app_processing",
            "routing_key": "celery_app_processing",
        },
    }


# Create Celery application
celery_app = Celery(
    "fastapi_celery_worker", include=["celery_app.tasks.celery_app_processing_tasks"]
)

# Apply configuration
celery_app.config_from_object(Config)

if __name__ == "__main__":
    celery_app.start()
