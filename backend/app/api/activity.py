"""Activity feed built from the user's real events."""

from __future__ import annotations

from fastapi import APIRouter, Query

from app.services.activity import get_activity_feed
from app.store import store

router = APIRouter(tags=["activity"])


@router.get("/activity/{user_id}")
def get_activity(user_id: int, limit: int = Query(10, ge=1, le=100)):
    return {"user_id": user_id, "activities": get_activity_feed(store.events(user_id), limit)}
