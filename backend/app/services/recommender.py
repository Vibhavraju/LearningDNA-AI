"""Recommender: turns knowledge gaps + forgetting into a ranked study plan."""

from __future__ import annotations

from typing import Any


def build_gaps(dna: dict[str, Any]) -> list[dict[str, Any]]:
    """Rank topics by priority = weak mastery (60%) + low predicted retention (40%)."""
    gaps = []
    for topic, s in dna.get("topic_mastery", {}).items():
        priority = 0.6 * (1 - s["mastery"]) + 0.4 * (1 - s["retention"])
        gaps.append({"topic_name": topic, "mastery": s["mastery"], "retention": s["retention"],
                     "priority": round(priority, 3)})
    return sorted(gaps, key=lambda g: g["priority"], reverse=True)


def generate_recommendations(user_id: int, gaps: list[dict[str, Any]], daily_budget_min: int = 90,
                             attention_min: float | None = None) -> list[dict[str, Any]]:
    """Build up to 5 tasks that fit the daily budget; session length respects attention span."""
    cap = int(min(25, attention_min)) if attention_min and attention_min >= 10 else 25
    tasks: list[dict[str, Any]] = []
    used = 0
    for gap in gaps[:5]:
        if used >= daily_budget_min:
            break
        mastery, retention = gap.get("mastery", 0.0), gap.get("retention", 1.0)
        name = gap.get("topic_name", "Topic")
        if mastery < 0.4:
            kind, title = "learn", f"Learn {name} fundamentals"
            reason = f"Low mastery ({mastery:.0%}) - build the basics first"
        elif retention < 0.6:
            kind, title = "revise", f"Revise {name}"
            reason = f"Predicted retention has dropped to {retention:.0%}"
        else:
            kind, title = "practice", f"Practice {name} problems"
            reason = f"Mastery {mastery:.0%} - practice to consolidate"
        minutes = min(cap, daily_budget_min - used)
        tasks.append({"id": len(tasks) + 1, "rank": len(tasks) + 1, "task_type": kind, "topic": name,
                      "title": f"{title} ({minutes} min)", "minutes": minutes,
                      "reason": reason, "status": "pending"})
        used += minutes
    return tasks
