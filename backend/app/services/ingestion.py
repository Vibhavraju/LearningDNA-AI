"""Event ingestion: validate, normalise and (optionally) store events."""

from __future__ import annotations

from typing import Any

from app.services.features import parse_ts

REQUIRED = ("user_id", "ts", "type")
VALID_TYPES = {"session", "quiz_answer", "content_view"}


def normalise_event(event: dict[str, Any]) -> dict[str, Any]:
    """Return a clean event or raise ValueError describing the problem."""
    missing = [f for f in REQUIRED if f not in event]
    if missing:
        raise ValueError(f"missing fields: {', '.join(missing)}")
    if event["type"] not in VALID_TYPES:
        raise ValueError(f"unknown type '{event['type']}' (expected one of {sorted(VALID_TYPES)})")
    try:
        user_id = int(event["user_id"])
        ts = parse_ts(event["ts"])
    except (TypeError, ValueError) as exc:
        raise ValueError(f"invalid user_id/ts: {exc}") from exc
    payload = event.get("payload") or {}
    if not isinstance(payload, dict):
        raise ValueError("payload must be an object")
    return {"user_id": user_id, "ts": ts, "type": event["type"],
            "topic": event.get("topic") or event.get("topic_id"), "payload": payload}


def ingest_events(events: list[dict[str, Any]], store=None) -> dict[str, Any]:
    """Validate a batch; store accepted events if a store is given."""
    accepted, errors = [], []
    for i, ev in enumerate(events):
        try:
            accepted.append(normalise_event(ev))
        except ValueError as exc:
            errors.append({"index": i, "error": str(exc)})
    if store is not None:
        for ev in accepted:
            store.add_event(ev["user_id"], ev)
    return {"accepted": len(accepted), "rejected": len(errors), "total": len(events),
            "errors": errors, "user_ids": sorted({e["user_id"] for e in accepted})}
