"""Bayesian Knowledge Tracing (BKT) with a proper forward pass and parameter fitting."""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize

_EPS = 1e-9


class BKT:
    """Standard 4-parameter BKT (init, learn, guess, slip). Mastery is absorbing (no forgetting)."""

    def __init__(self, p_init: float = 0.1, p_learn: float = 0.1,
                 p_guess: float = 0.1, p_slip: float = 0.05):
        self.p_init = p_init
        self.p_learn = p_learn
        self.p_guess = p_guess
        self.p_slip = p_slip

    def params(self) -> tuple[float, float, float, float]:
        return self.p_init, self.p_learn, self.p_guess, self.p_slip

    def forward(self, correct) -> tuple[np.ndarray, np.ndarray]:
        """Return (P(mastered) after each observation, log-likelihood of each observation)."""
        correct = np.asarray(correct, dtype=float)
        n = len(correct)
        mastery = np.zeros(n)
        loglik = np.zeros(n)
        p_m = float(np.clip(self.p_init, _EPS, 1 - _EPS))
        for i, c in enumerate(correct):
            p_correct = p_m * (1 - self.p_slip) + (1 - p_m) * self.p_guess
            p_correct = float(np.clip(p_correct, _EPS, 1 - _EPS))
            if c >= 0.5:
                loglik[i] = np.log(p_correct)
                posterior = p_m * (1 - self.p_slip) / p_correct
            else:
                loglik[i] = np.log(1 - p_correct)
                posterior = p_m * self.p_slip / (1 - p_correct)
            mastery[i] = posterior
            # learning transition: once mastered, stays mastered
            p_m = float(np.clip(posterior + (1 - posterior) * self.p_learn, _EPS, 1 - _EPS))
        return mastery, loglik

    def predict_correct(self, correct) -> float:
        """Probability the *next* answer is correct, given history."""
        correct = np.asarray(correct, dtype=float)
        if len(correct) == 0:
            p_m = self.p_init
        else:
            mastery, _ = self.forward(correct)
            p_m = mastery[-1] + (1 - mastery[-1]) * self.p_learn
        return float(p_m * (1 - self.p_slip) + (1 - p_m) * self.p_guess)

    def fit(self, correct, max_iter: int = 50) -> "BKT":
        """Maximum-likelihood fit with bounds (guess<=0.3, slip<=0.3 avoids degenerate fits)."""
        correct = np.asarray(correct, dtype=float)
        if len(correct) < 3:
            return self

        def neg_ll(theta: np.ndarray) -> float:
            m = BKT(*theta)
            _, ll = m.forward(correct)
            return -float(ll.sum())

        x0 = np.array(self.params())
        bounds = [(0.01, 0.9), (0.01, 0.6), (0.01, 0.3), (0.01, 0.3)]
        res = minimize(neg_ll, x0, method="L-BFGS-B", bounds=bounds, options={"maxiter": max_iter})
        if res.success or np.isfinite(res.fun):
            self.p_init, self.p_learn, self.p_guess, self.p_slip = (float(v) for v in res.x)
        return self
