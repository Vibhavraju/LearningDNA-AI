"""Feature engineering: turns raw events into per-user features for the DNA model."""

from __future__ import annotations

import math
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

import numpy as np

from app.ml.attention import detect_attention_change_point
from app.ml.bkt import BKT
from app.ml.forgetting import fit_stability, forgetting_curve


def parse_ts(value: Any) -> datetime:
    if isinstance(value, datetime):
        dt = value
    else:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def _fmt_hour(h: int) -> str:
    h %= 24
    return f"{(h % 12) or 12}:00 {'AM' if h < 12 else 'PM'}"


def compute_features(events: list[dict[str, Any]], now: datetime | None = None,
                     window_days: int = 28) -> dict[str, Any]:
    now = now or datetime.now(timezone.utc)
    evs = sorted(({**e, "ts": parse_ts(e["ts"])} for e in events if e.get("ts")), key=lambda e: e["ts"])
    evs = [e for e in evs if e["ts"] <= now]
    quiz = [e for e in evs if e["type"] == "quiz_answer"]
    sessions = [e for e in evs if e["type"] == "session"]
    views = [e for e in evs if e["type"] == "content_view"]

    # ---- daily minutes (zeros included) ----
    if evs:
        span_days = max(7, min(window_days, (now - evs[0]["ts"]).days + 1))
    else:
        span_days = 7
    daily = np.zeros(span_days)
    for s in sessions:
        age = (now.date() - s["ts"].date()).days
        if 0 <= age < span_days:
            daily[span_days - 1 - age] += float(s.get("payload", {}).get("duration_min", 0))

    # ---- per-topic BKT + retention ----
    by_topic: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for q in quiz:
        by_topic[str(q.get("topic", "General"))].append(q)

    topic_stats: dict[str, dict[str, float]] = {}
    attempts_to_master: list[float] = []
    stabilities: list[float] = []
    for topic, qs in by_topic.items():
        correct = np.array([1.0 if q.get("payload", {}).get("correct") else 0.0 for q in qs])
        bkt = BKT()
        if len(correct) >= 8:
            bkt.fit(correct)
        mastery_seq, _ = bkt.forward(correct)
        mastery = float(mastery_seq[-1])
        hit = np.where(mastery_seq >= 0.9)[0]
        attempts_to_master.append(float(hit[0] + 1) if len(hit) else min(20.0, len(correct) * 1.5))

        # review days -> gaps and performance
        per_day: dict[Any, list[float]] = defaultdict(list)
        for q, c in zip(qs, correct):
            per_day[q["ts"].date()].append(c)
        days_sorted = sorted(per_day)
        gaps = [(days_sorted[i] - days_sorted[i - 1]).days for i in range(1, len(days_sorted))]
        perf = [float(np.mean(per_day[days_sorted[i]])) >= 0.6 for i in range(1, len(days_sorted))]
        stability = fit_stability(gaps, perf)
        stabilities.append(stability)
        days_since = (now - qs[-1]["ts"]).total_seconds() / 86400
        retention = forgetting_curve(days_since, stability)
        topic_stats[topic] = {
            "mastery": mastery, "retention": retention, "stability_days": stability,
            "attempts": float(len(correct)), "accuracy": float(correct.mean()),
            "days_since_review": days_since,
        }

    # ---- speed inputs ----
    total_hours = float(daily.sum()) / 60.0
    n_topics = max(len(topic_stats), 1)
    mean_mastery = float(np.mean([t["mastery"] for t in topic_stats.values()])) if topic_stats else 0.0
    hours_per_topic = max(total_hours / n_topics, 0.25)
    gain_per_hour = max(mean_mastery - 0.1, 0.0) / hours_per_topic

    # ---- attention ----
    spans = []
    for s in sessions:
        eng = s.get("payload", {}).get("engagement")
        if eng:
            spans.append(detect_attention_change_point(eng))
        elif s.get("payload", {}).get("duration_min"):
            spans.append(float(s["payload"]["duration_min"]))
    attention_span_min = float(np.mean(spans)) if spans else 0.0
    durations = [float(s.get("payload", {}).get("duration_min", 0)) for s in sessions]

    # ---- best study hour window ----
    hour_ok: dict[int, list[float]] = defaultdict(list)
    for q in quiz:
        hour_ok[q["ts"].hour].append(1.0 if q.get("payload", {}).get("correct") else 0.0)
    best_window = None
    best_score = -1.0
    for h in range(24):
        hs = [(h + k) % 24 for k in range(3)]
        vals = [v for x in hs for v in hour_ok.get(x, [])]
        if len(vals) < 6:
            continue
        score = sum(vals) / (len(vals) + 2)
        if score > best_score:
            best_score, best_window = score, h
    best_time = f"{_fmt_hour(best_window)} - {_fmt_hour(best_window + 3)}" if best_window is not None else "Not enough data"

    # ---- preferred format ----
    fmt_counts: dict[str, float] = defaultdict(float)
    for v in views:
        fmt_counts[str(v.get("payload", {}).get("format", "reading"))] += float(v.get("payload", {}).get("completion", 1.0))
    label = {"video": "Visual", "practice": "Practice", "reading": "Reading", "quiz": "Quiz"}
    top = sorted(fmt_counts, key=fmt_counts.get, reverse=True)[:2]
    preferred_format = " + ".join(label.get(f, f.title()) for f in top) if top else "Not enough data"

    n_quiz, n_sessions = len(quiz), len(sessions)
    confidence = 100 * (1 - math.exp(-(n_quiz / 60 + n_sessions / 12))) if (n_quiz or n_sessions) else 0.0

    return {
        "n_quiz": n_quiz, "n_sessions": n_sessions, "daily_minutes": daily,
        "quiz_accuracy": (sum(1 for q in quiz if q.get("payload", {}).get("correct")) / n_quiz) if n_quiz else 0.0,
        "topic_stats": topic_stats,
        "mean_stability": float(np.mean(stabilities)) if stabilities else 3.0,
        "gain_per_hour": gain_per_hour,
        "attempts_to_mastery": float(np.mean(attempts_to_master)) if attempts_to_master else 15.0,
        "attention_span_min": attention_span_min,
        "avg_session_min": float(np.mean(durations)) if durations else 0.0,
        "best_time": best_time, "preferred_format": preferred_format,
        "confidence": min(95.0, confidence),
        "active_days": int((daily > 0).sum()), "window_days": int(span_days),
    }
