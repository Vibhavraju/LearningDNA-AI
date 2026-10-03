"""Celery task definitions. Tasks take optional arguments so the beat schedule can call them bare."""

from __future__ import annotations

from app.workers.celery_app import celery_app


def _user_ids(user_id: int | None) -> list[int]:
    from app.store import store

    return [user_id] if user_id is not None else (list(store._users) or [1])  # noqa: SLF001


@celery_app.task(name="app.workers.tasks.incremental_update")
def incremental_update(user_id: int, topic_ids: list | None = None) -> dict:
    """Refresh DNA after new events for a user."""
    from app.store import store

    dna = store.get_dna(user_id, force=True)
    return {"user_id": user_id, "overall": dna["overall"]}


@celery_app.task(name="app.workers.tasks.nightly_recompute")
def nightly_recompute(user_id: int | None = None) -> dict:
    """Full recompute of all DNA dimensions (all users when no id given)."""
    from app.store import store

    return {uid: store.get_dna(uid, force=True)["overall"] for uid in _user_ids(user_id)}


@celery_app.task(name="app.workers.tasks.weekly_snapshot")
def weekly_snapshot(user_id: int | None = None) -> dict:
    """Store a weekly DNA snapshot for trend history."""
    from app.store import store

    return {uid: store.recompute_dna(uid)["overall"] for uid in _user_ids(user_id)}


@celery_app.task(name="app.workers.tasks.retrain_dkt")
def retrain_dkt() -> dict:
    """Retrain the DKT model on simulated data (needs PyTorch)."""
    from ml.train_dkt import train_dkt_pipeline

    return train_dkt_pipeline()
