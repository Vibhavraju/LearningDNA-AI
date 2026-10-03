"""Student simulator: generates realistic study events from a persona.

Used to seed the demo user, to build the cohort for percentile scoring, and by the
`simulator` package. Deterministic for a given seed.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any

TOPICS = [
    "Python Basics", "SQL", "Statistics", "Recursion",
    "Dynamic Programming", "Probability", "MapReduce", "Neural Networks",
]


@dataclass
class Persona:
    name: str
    learning_rate: float          # 0-1, how fast mastery grows per attempt
    forgetting_stability: float   # 0-1, higher = forgets slower
    attention_span: int           # minutes before engagement drops
    best_hour_start: int
    best_hour_end: int
    format_affinity: dict[str, float] = field(default_factory=dict)
    consistency: float = 0.7      # probability of studying on a given day


STUDENT_A = Persona("Alex", 0.8, 0.9, 45, 19, 22, {"video": 0.5, "practice": 0.3, "reading": 0.2}, 0.8)
STUDENT_B = Persona("Bob", 0.4, 0.4, 25, 8, 11, {"reading": 0.6, "quiz": 0.2, "video": 0.2}, 0.5)
STUDENT_C = Persona("Cara", 0.6, 0.7, 60, 14, 17, {"reading": 0.5, "practice": 0.4, "video": 0.1}, 0.9)
PERSONAS = [STUDENT_A, STUDENT_B, STUDENT_C]


def generate_events(persona: Persona, user_id: int = 1, days: int = 28,
                    seed: int = 42, now: datetime | None = None,
                    topics: list[str] | None = None) -> list[dict[str, Any]]:
    """Generate session / quiz_answer / content_view events for `days` days ending at `now`."""
    rng = random.Random(seed)
    now = now or datetime.now(timezone.utc)
    topics = topics or TOPICS
    mastery = {t: 0.15 + 0.15 * rng.random() for t in topics}
    last_seen: dict[str, datetime] = {}
    events: list[dict[str, Any]] = []
    stability_days = 2 + 18 * persona.forgetting_stability

    for d in range(days, 0, -1):
        day = (now - timedelta(days=d)).replace(minute=0, second=0, microsecond=0)
        if rng.random() > persona.consistency:
            continue
        hour = rng.randint(persona.best_hour_start, max(persona.best_hour_start, persona.best_hour_end - 1))
        start = day.replace(hour=hour)
        duration = max(10.0, persona.attention_span * rng.uniform(0.7, 1.2))
        windows = max(3, int(duration // 5))
        engagement = []
        for w in range(windows):
            minutes_in = w * 5
            base = 0.9 if minutes_in < persona.attention_span else 0.9 * math.exp(-(minutes_in - persona.attention_span) / 15)
            engagement.append(round(min(1.0, max(0.05, base + rng.uniform(-0.05, 0.05))), 3))
        events.append({"user_id": user_id, "ts": start, "type": "session",
                       "payload": {"duration_min": round(duration, 1), "engagement": engagement}})

        session_topics = rng.sample(topics, k=2)
        fmts, weights = zip(*persona.format_affinity.items()) if persona.format_affinity else (("reading",), (1.0,))
        for t in session_topics:
            fmt = rng.choices(fmts, weights=weights)[0]
            events.append({"user_id": user_id, "ts": start + timedelta(minutes=1), "type": "content_view",
                           "topic": t, "payload": {"format": fmt, "completion": round(rng.uniform(0.6, 1.0), 2)}})
            # forgetting since last time
            if t in last_seen:
                gap = (start - last_seen[t]).total_seconds() / 86400
                mastery[t] *= math.exp(-gap / stability_days)
            n_q = rng.randint(3, 5)
            for q in range(n_q):
                p_correct = mastery[t] * 0.92 + (1 - mastery[t]) * 0.25
                correct = rng.random() < p_correct
                events.append({"user_id": user_id, "ts": start + timedelta(minutes=3 + q * 2 + (0 if t == session_topics[0] else 12)),
                               "type": "quiz_answer", "topic": t,
                               "payload": {"correct": correct, "response_time_s": round(rng.uniform(12, 55) * (1.4 - persona.learning_rate), 1)}})
                mastery[t] = min(0.99, mastery[t] + persona.learning_rate * 0.2 * (1 - mastery[t]) * (1.0 if correct else 0.5))
            last_seen[t] = start
    events.sort(key=lambda e: e["ts"])
    return events
