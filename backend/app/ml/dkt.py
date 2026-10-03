"""Deep Knowledge Tracing (LSTM). PyTorch is imported lazily so the API runs without it."""

from __future__ import annotations

import numpy as np


def _torch():
    try:
        import torch  # noqa: WPS433
        import torch.nn as nn  # noqa: WPS433
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("PyTorch not installed. Run: pip install -r requirements-ml.txt") from exc
    return torch, nn


def encode_interactions(topic_ids, correct, num_topics: int) -> np.ndarray:
    """One-hot (topic, correct) encoding of size 2*num_topics per step."""
    x = np.zeros((len(topic_ids), 2 * num_topics), dtype=np.float32)
    for i, (t, c) in enumerate(zip(topic_ids, correct)):
        x[i, int(t) + (num_topics if c else 0)] = 1.0
    return x


def build_model(num_topics: int = 50, hidden_size: int = 64):
    torch, nn = _torch()

    class DKTModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.num_topics = num_topics
            self.lstm = nn.LSTM(2 * num_topics, hidden_size, batch_first=True)
            self.fc = nn.Linear(hidden_size, num_topics)

        def forward(self, x):  # (B, T, 2K) -> (B, T, K) probabilities of correct per topic
            out, _ = self.lstm(x)
            return torch.sigmoid(self.fc(out))

    return DKTModel()


def train_dkt(sequences, num_topics: int = 50, epochs: int = 10, lr: float = 1e-2):
    """sequences: list of (topic_ids, correct) pairs. Trains next-step prediction."""
    torch, nn = _torch()
    model = build_model(num_topics)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.BCELoss()
    data = [(encode_interactions(t, c, num_topics), np.asarray(t), np.asarray(c, dtype=np.float32))
            for t, c in sequences if len(t) >= 2]
    history = []
    for _ in range(epochs):
        total = 0.0
        for x, topics, correct in data:
            xt = torch.from_numpy(x[:-1]).unsqueeze(0)
            pred = model(xt)[0]  # (T-1, K)
            idx = torch.from_numpy(topics[1:]).long()
            p = pred[torch.arange(len(idx)), idx]
            y = torch.from_numpy(correct[1:])
            loss = loss_fn(p, y)
            opt.zero_grad()
            loss.backward()
            opt.step()
            total += float(loss)
        history.append(total / max(len(data), 1))
    return model, history


def predict_mastery_dkt(model, x: np.ndarray) -> np.ndarray:
    torch, _ = _torch()
    model.eval()
    with torch.no_grad():
        out = model(torch.from_numpy(np.asarray(x, dtype=np.float32)).unsqueeze(0))
    return out.squeeze(0).numpy()
