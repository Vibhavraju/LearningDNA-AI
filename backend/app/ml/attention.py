"""Attention span estimation from per-window engagement scores."""

from __future__ import annotations

import numpy as np


def detect_attention_change_point(engagement, window_sec: int = 300,
                                  drop_threshold: float = 0.2) -> float:
    """Return attention span in minutes: when engagement first drops `drop_threshold`
    below the opening baseline (first 3 windows) for 3 consecutive windows."""
    eng = np.asarray(engagement, dtype=float)
    n = len(eng)
    if n == 0:
        return 0.0
    baseline = float(np.mean(eng[: min(3, n)]))
    if baseline < 0.3:
        return 0.0
    for i in range(min(3, n), n):
        if float(np.mean(eng[i: i + 3])) < baseline * (1 - drop_threshold):
            return i * window_sec / 60.0
    return n * window_sec / 60.0
