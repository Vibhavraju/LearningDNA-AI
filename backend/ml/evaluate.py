"""Evaluate BKT (and DKT if PyTorch is installed) at predicting the next answer.

Run:  cd backend && python -m ml.evaluate
"""

from __future__ import annotations

import numpy as np
from sklearn.metrics import accuracy_score, mean_squared_error, roc_auc_score

from app.ml.bkt import BKT
from ml.train_dkt import build_sequences


def _metrics(y: np.ndarray, p: np.ndarray) -> dict[str, float]:
    return {
        "auc": float(roc_auc_score(y, p)) if len(np.unique(y)) > 1 else 0.5,
        "rmse": float(np.sqrt(mean_squared_error(y, p))),
        "accuracy": float(accuracy_score(y, (p > 0.5).astype(int))),
    }


def evaluate_bkt(seqs) -> dict[str, float]:
    """Per (student, topic): fit BKT on the first 70% of answers, predict the remaining 30% one step ahead."""
    ys, ps = [], []
    for topics, correct in seqs:
        for t in set(topics):
            c = np.array([x for tt, x in zip(topics, correct) if tt == t], dtype=float)
            if len(c) < 10:
                continue
            split = int(len(c) * 0.7)
            model = BKT().fit(c[:split])
            for i in range(split, len(c)):
                ps.append(model.predict_correct(c[:i]))
                ys.append(c[i])
    return _metrics(np.array(ys), np.array(ps))


def evaluate_retention_prediction(predicted: np.ndarray, actual: np.ndarray) -> dict[str, float]:
    return {"retention_mae": float(np.mean(np.abs(predicted - actual)))}


def evaluate_trait_recovery(recovered: dict, true: dict) -> dict[str, float]:
    return {f"{k}_error": abs(recovered[k] - v) for k, v in true.items() if k in recovered}


if __name__ == "__main__":
    seqs = build_sequences(30)
    print("BKT next-answer prediction:", evaluate_bkt(seqs))
