"""Explainability: why did a DNA dimension change?"""

from __future__ import annotations

from typing import Any

DIMENSIONS = ["speed", "retention", "attention", "quiz", "consistency"]

_FEATURE_TEXT = {
    "speed": "attempts needed to master topics and mastery gained per study hour",
    "retention": "predicted forgetting and how recently topics were reviewed",
    "attention": "how long engagement stays high in a session",
    "quiz": "quiz accuracy",
    "consistency": "how many days you studied and how even the sessions were",
}


def explain_dimension_change(dimension: str, old_value: float, new_value: float,
                             contributing_features: list[str]) -> dict[str, Any]:
    delta = new_value - old_value
    direction = "improved" if delta > 0 else "declined" if delta < 0 else "unchanged"
    reason = (f"{dimension.title()} {direction}" +
              (f" by {abs(round(delta))} points" if delta else "") +
              (f", driven by {', '.join(contributing_features)}." if contributing_features else "."))
    return {
        "dimension": dimension, "old_value": round(old_value), "new_value": round(new_value),
        "delta": round(delta), "direction": direction,
        "contributing_features": contributing_features, "reason": reason,
    }


def explain_snapshots(old: dict[str, Any] | None, new: dict[str, Any]) -> dict[str, Any]:
    old = old or new
    return {d: explain_dimension_change(d, old.get(d, 0), new.get(d, 0), [_FEATURE_TEXT[d]])
            for d in DIMENSIONS}


def generate_learning_narrative(dna: dict[str, Any]) -> str:
    strong = (dna.get("strong_topics") or ["core concepts"])[0]
    gap = (dna.get("weak_topics") or ["no clear gap yet"])[0]
    return (f"Your strongest performance is in {strong}. "
            f"You learn {'quickly' if dna.get('speed', 0) > 70 else 'at a steady pace'}. "
            f"Your largest knowledge gap is {gap}. "
            f"{dna.get('traits', {}).get('preferred_format', 'Mixed')} material works best for you.")
