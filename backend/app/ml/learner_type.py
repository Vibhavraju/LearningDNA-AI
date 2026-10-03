"""Learner archetype classification (nearest-centroid; optional fitted GMM)."""

from __future__ import annotations

import numpy as np

LEARNER_TYPES = [
    "Visual-Practice Learner",
    "Reading-Deep Learner",
    "Fast-Intuitive Learner",
    "Steady-Consolidator",
    "Burst-Crammer",
]

# centroids in [speed, retention, attention, quiz, consistency] (0-1)
_CENTROIDS = np.array([
    [0.75, 0.70, 0.80, 0.80, 0.70],  # Visual-Practice
    [0.45, 0.80, 0.85, 0.70, 0.75],  # Reading-Deep
    [0.90, 0.55, 0.60, 0.80, 0.50],  # Fast-Intuitive
    [0.55, 0.80, 0.65, 0.65, 0.90],  # Steady-Consolidator
    [0.70, 0.35, 0.45, 0.60, 0.25],  # Burst-Crammer
])


def classify_learner_type(dna_vector, model=None) -> str:
    """Classify a DNA vector. Uses `model` (fitted GaussianMixture) if given,
    otherwise the nearest archetype centroid on the first five dimensions."""
    vec = np.asarray(dna_vector, dtype=float).reshape(-1)
    if model is not None:
        label = int(model.predict(vec.reshape(1, -1))[0])
        return LEARNER_TYPES[label % len(LEARNER_TYPES)]
    v = vec[:5]
    dists = np.linalg.norm(_CENTROIDS - v, axis=1)
    return LEARNER_TYPES[int(np.argmin(dists))]
