"""Event ingestion: validates a batch, stores it, refreshes the DNA and notifies websocket clients."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from app.api.ws import manager
from app.services.ingestion import ingest_events
from app.store import store

router = APIRouter(tags=["events"])


@router.post("/events")
async def create_events(events: list[dict[str, Any]]):
    if not events:
        raise HTTPException(status_code=422, detail="Send a non-empty list of events")
    if len(events) > 1000:
        raise HTTPException(status_code=413, detail="Max 1000 events per batch")
    result = ingest_events(events, store)
    for uid in result["user_ids"]:
        dna = store.get_dna(uid, force=True)
        await manager.broadcast_dna_update(uid, {"overall": dna["overall"], "confidence": dna["confidence"]})
    return {"message": "Events accepted" if result["accepted"] else "No valid events", **result}
