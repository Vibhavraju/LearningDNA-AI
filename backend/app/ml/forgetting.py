"""Forgetting curve: R(t) = exp(-t / S)."""

from __future__ import annotations

import math

import numpy as np

LN2 = math.log(2)


def forgetting_curve(t: float, stability: float) -> float:
    """Predicted retention after `t` days with stability `stability` (days)."""
    if stability <= 0:
        return 0.0
    return float(math.exp(-max(t, 0.0) / stability))


def fit_stability(review_gaps, performance) -> float:
    """Estimate stability (days) from gaps between reviews and whether recall succeeded.

    A successful recall after a gap `t` implies R(t) >= 0.5  ->  S >= t / ln 2.
    With no successes we assume S is short (a failed recall at gap `t` implies S < t / ln 2).
    """
    gaps = np.asarray(review_gaps, dtype=float)
    perf = np.asarray(performance, dtype=float)
    if len(gaps) == 0:
        return 3.0
    ok = gaps[perf >= 0.5]
    if len(ok) > 0:
        s = float(np.mean(ok)) / LN2
    else:
        s = 0.7 * float(np.mean(gaps)) / LN2
    return float(np.clip(s, 2.0, 60.0))
