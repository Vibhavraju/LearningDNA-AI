"""Learning speed score."""

from __future__ import annotations

import numpy as np


def compute_learning_speed(mastery_gain_per_hour: float, attempts_to_mastery: float,
                           cohort_percentile: float) -> float:
    """Score 0-100.

    mastery_gain_per_hour: mastery gained per study hour (0.4+ is excellent)
    attempts_to_mastery:   average attempts needed (3 is excellent, 15+ is slow)
    cohort_percentile:     0-1 position versus the simulated cohort
    """
    gain = float(np.clip(mastery_gain_per_hour / 0.4, 0, 1))
    attempts = float(np.clip(1 - (attempts_to_mastery - 3) / 12, 0, 1))
    pct = float(np.clip(cohort_percentile, 0, 1))
    return float(np.clip(100 * (0.4 * gain + 0.3 * attempts + 0.3 * pct), 0, 100))


def pace_label(speed: float) -> str:
    if speed < 40:
        return "Slow"
    if speed < 70:
        return "Moderate"
    return "Fast"
