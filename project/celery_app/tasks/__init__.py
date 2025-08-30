"""
Celery tasks package for distributed task processing.

This package contains all Celery task definitions for background processing.
"""

from .celery_app_processing_tasks import create_task

__all__ = ["create_task"]
