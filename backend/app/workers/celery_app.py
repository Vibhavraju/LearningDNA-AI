"""Celery app configuration (broker/backend come from env, defaults for local dev)."""

import os

from celery import Celery
from celery.schedules import crontab

import app.config  # noqa: F401  (loads .env)

celery_app = Celery(
    "dna_ai",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/1"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/2"),
    include=["app.workers.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_always_eager=os.getenv("CELERY_TASK_ALWAYS_EAGER", "false").lower() == "true",
)

celery_app.conf.beat_schedule = {
    "nightly-recompute": {"task": "app.workers.tasks.nightly_recompute", "schedule": crontab(hour=2, minute=0)},
    "weekly-snapshot": {"task": "app.workers.tasks.weekly_snapshot", "schedule": crontab(hour=3, minute=0, day_of_week=0)},
}
