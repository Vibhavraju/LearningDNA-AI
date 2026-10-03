"""Per-user settings (DNA weights, daily study budget, ...)."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.schemas import SettingsUpdate
from app.store import store

router = APIRouter(tags=["settings"])
DIMS = {"speed", "retention", "attention", "quiz", "consistency"}


@router.get("/settings/{user_id}")
def get_settings(user_id: int):
    return {"user_id": user_id, **store.user(user_id).settings}


@router.put("/settings/{user_id}")
def update_settings(user_id: int, update: SettingsUpdate):
    st = store.user(user_id)
    data = update.model_dump(exclude_none=True)
    if "dna_weights" in data:
        if not set(data["dna_weights"]) <= DIMS or any(v < 0 for v in data["dna_weights"].values()):
            raise HTTPException(status_code=422, detail=f"dna_weights keys must be in {sorted(DIMS)} and non-negative")
    st.settings.update(data)
    if "dna_weights" in data:
        store.get_dna(user_id, force=True)
    return {"user_id": user_id, **st.settings}
