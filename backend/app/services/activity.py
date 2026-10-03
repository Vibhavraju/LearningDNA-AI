"""Activity feed built from real events."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

from app.services.features import parse_ts


def relative_time(ts: datetime, now: datetime) -> str:
    secs = max(0, int((now - ts).total_seconds()))
    if secs < 3600:
        m = max(1, secs // 60)
        return f"{m} minute{'s' if m != 1 else ''} ago"
    if secs < 86400:
        h = secs // 3600
        return f"{h} hour{'s' if h != 1 else ''} ago"
    d = secs // 86400
    return f"{d} day{'s' if d != 1 else ''} ago"


def get_activity_feed(events: list[dict[str, Any]], limit: int = 10,
                      now: datetime | None = None) -> list[dict[str, Any]]:
    now = now or datetime.now(timezone.utc)
    items: list[dict[str, Any]] = []
    quiz_groups: dict[tuple, list[dict[str, Any]]] = defaultdict(list)
    for e in events:
        ts = parse_ts(e["ts"])
        if ts > now:
            continue
        if e["type"] == "quiz_answer":
            quiz_groups[(ts.date(), e.get("topic", "General"))].append({**e, "ts": ts})
        elif e["type"] == "content_view":
            fmt = e.get("payload", {}).get("format", "reading")
            verb = {"video": "Watched", "practice": "Practiced", "reading": "Read"}.get(fmt, "Studied")
            pct = int(float(e.get("payload", {}).get("completion", 1)) * 100)
            items.append({"type": fmt, "title": f"{verb} {e.get('topic', 'a topic')}", "detail": f"{pct}%",
                          "ts": ts, "icon": {"video": "play", "practice": "code"}.get(fmt, "book")})
    for (_, topic), qs in quiz_groups.items():
        ok = sum(1 for q in qs if q.get("payload", {}).get("correct"))
        items.append({"type": "quiz", "title": f"Completed {topic} Quiz", "detail": f"{ok}/{len(qs)}",
                      "ts": max(q["ts"] for q in qs), "icon": "check-circle"})
    items.sort(key=lambda i: i["ts"], reverse=True)
    out = []
    for i in items[:limit]:
        rel = relative_time(i["ts"], now)
        out.append({"type": i["type"], "title": i["title"], "detail": i["detail"], "time": rel,
                    "relative_time": rel, "timestamp": i["ts"].isoformat(), "icon": i["icon"]})
    return out
