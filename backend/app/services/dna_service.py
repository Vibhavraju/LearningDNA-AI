"""DNA service: assembles the five ML dimensions into a learner profile."""

from __future__ import annotations

import random
from datetime import datetime, timezone
from functools import lru_cache
from typing import Any

import numpy as np

from app.ml.consistency import compute_consistency, consistency_label
from app.ml.learner_type import classify_learner_type
from app.ml.speed import compute_learning_speed, pace_label
from app.services.features import compute_features

DEFAULT_WEIGHTS = {"speed": 0.25, "retention": 0.30, "attention": 0.10, "quiz": 0.15, "consistency": 0.20}


def _normalise_weights(weights: dict[str, float] | None) -> dict[str, float]:
    w = {**DEFAULT_WEIGHTS, **(weights or {})}
    total = sum(max(v, 0.0) for v in w.values())
    if total <= 0:
        return dict(DEFAULT_WEIGHTS)
    return {k: max(v, 0.0) / total for k, v in w.items()}


def assemble_dna(speed: float, retention: float, attention: float, quiz_accuracy: float,
                 consistency: float, weights: dict[str, float] | None = None,
                 confidence: float = 50.0) -> dict[str, Any]:
    """Combine individual dimensions (each 0-100) into an overall DNA profile."""
    w = _normalise_weights(weights)
    overall = (speed * w["speed"] + retention * w["retention"] + attention * w["attention"]
               + quiz_accuracy * w["quiz"] + consistency * w["consistency"])
    vec = np.array([speed, retention, attention, quiz_accuracy, consistency]) / 100.0
    return {
        "speed": speed, "retention": retention, "attention": attention,
        "quiz": quiz_accuracy, "quiz_accuracy": quiz_accuracy, "consistency": consistency,
        "overall": int(round(overall)),
        "pace": pace_label(speed),
        "consistency_label": consistency_label(consistency),
        "learner_type": classify_learner_type(vec),
        "dna_vector": vec.tolist(),
        "confidence": int(round(confidence)),
    }


def _raw_speed_signal(gain_per_hour: float, attempts: float) -> float:
    gain = float(np.clip(gain_per_hour / 0.4, 0, 1))
    att = float(np.clip(1 - (attempts - 3) / 12, 0, 1))
    return 0.5 * gain + 0.5 * att


@lru_cache(maxsize=1)
def _cohort_signals() -> tuple[float, ...]:
    """Speed signal for a fixed simulated cohort (used for the percentile)."""
    from app.simulation import Persona, generate_events

    rng = random.Random(7)
    ref = datetime(2026, 1, 1, tzinfo=timezone.utc)
    signals = []
    for i in range(15):
        p = Persona(f"c{i}", rng.uniform(0.2, 0.95), rng.uniform(0.2, 0.95), rng.randint(20, 70),
                    rng.randint(7, 20), 23, {"reading": 0.5, "video": 0.5}, rng.uniform(0.4, 0.95))
        f = compute_features(generate_events(p, 1000 + i, 28, seed=i, now=ref), now=ref)
        signals.append(_raw_speed_signal(f["gain_per_hour"], f["attempts_to_mastery"]))
    return tuple(sorted(signals))


def _percentile(signal: float) -> float:
    cohort = _cohort_signals()
    return sum(1 for c in cohort if c <= signal) / len(cohort)


def compute_dna(events: list[dict[str, Any]], user_id: int = 1, now: datetime | None = None,
                weights: dict[str, float] | None = None) -> dict[str, Any]:
    """Compute the full Learning DNA profile for a user from raw events."""
    now = now or datetime.now(timezone.utc)
    f = compute_features(events, now)
    stats = f["topic_stats"]

    if f["n_quiz"] == 0:
        speed = retention = quiz = 0.0
    else:
        signal = _raw_speed_signal(f["gain_per_hour"], f["attempts_to_mastery"])
        speed = compute_learning_speed(f["gain_per_hour"], f["attempts_to_mastery"], _percentile(signal))
        retention = 100 * float(np.mean([t["retention"] for t in stats.values()]))
        quiz = 100 * f["quiz_accuracy"]
    attention = float(np.clip(f["attention_span_min"] / 60 * 100, 0, 100))
    consistency = compute_consistency(f["daily_minutes"])

    dna = assemble_dna(speed, retention, attention, quiz, consistency, weights, f["confidence"])
    for k in ("speed", "retention", "attention", "quiz", "quiz_accuracy", "consistency"):
        dna[k] = int(round(dna[k]))

    ranked = sorted(stats.items(), key=lambda kv: kv[1]["mastery"])
    revision = "High" if f["mean_stability"] < 4 else "Medium" if f["mean_stability"] < 10 else "Low"
    dna.update({
        "user_id": user_id,
        "attention_span_min": round(f["attention_span_min"], 1),
        "weak_topics": [t for t, _ in ranked[:3]],
        "strong_topics": [t for t, _ in ranked[::-1][:3]],
        "topic_mastery": {t: {"mastery": round(s["mastery"], 3), "retention": round(s["retention"], 3),
                              "stability_days": round(s["stability_days"], 1),
                              "days_since_review": round(s["days_since_review"], 1)} for t, s in stats.items()},
        "traits": {
            "preferred_format": f["preferred_format"],
            "avg_session_duration": f"{round(f['avg_session_min'])} minutes",
            "best_study_time": f["best_time"],
            "revision_requirement": revision,
            "learning_pace": dna["pace"],
            "consistency": dna["consistency_label"],
        },
        "features": {
            "quiz_accuracy": round(f["quiz_accuracy"] * 100), "n_quiz": f["n_quiz"], "n_sessions": f["n_sessions"],
            "active_days": f["active_days"], "window_days": f["window_days"],
            "avg_attempts_to_mastery": round(f["attempts_to_mastery"], 1),
            "mean_stability_days": round(f["mean_stability"], 1),
            "attention_span_min": round(f["attention_span_min"], 1),
        },
        "computed_at": now.isoformat(),
    })
    return dna
