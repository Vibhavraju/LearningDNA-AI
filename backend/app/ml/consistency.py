"""Learning consistency: how regularly (and how evenly) a student studies."""

from __future__ import annotations

import numpy as np


def compute_consistency(daily_minutes) -> float:
    """Score 0-100 from study minutes per calendar day (include zero days).

    60% = share of days studied, 40% = evenness of session length on active days.
    """
    arr = np.asarray(daily_minutes, dtype=float)
    if arr.size == 0:
        return 0.0
    active = arr[arr > 0]
    if active.size == 0:
        return 0.0
    active_ratio = active.size / arr.size
    cv = float(np.std(active) / np.mean(active)) if np.mean(active) > 0 else 1.0
    regularity = 1.0 - min(cv, 1.0)
    return float(np.clip(100 * (0.6 * active_ratio + 0.4 * regularity), 0, 100))


def consistency_label(score: float) -> str:
    if score < 40:
        return "Poor"
    if score < 65:
        return "Fair"
    if score < 85:
        return "Good"
    return "Excellent"
