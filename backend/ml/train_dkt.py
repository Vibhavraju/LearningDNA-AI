"""Train the Deep Knowledge Tracing model on simulator data.

Run:  cd backend && python -m ml.train_dkt        (requires: pip install -r requirements-ml.txt)
"""

from __future__ import annotations

from app.ml.registry import ModelRegistry
from app.simulation import PERSONAS, TOPICS, generate_events


def build_sequences(n_students: int = 30) -> list[tuple[list[int], list[int]]]:
    seqs = []
    for i in range(n_students):
        persona = PERSONAS[i % len(PERSONAS)]
        events = generate_events(persona, user_id=i, days=28, seed=i)
        quiz = [e for e in events if e["type"] == "quiz_answer"]
        seqs.append(([TOPICS.index(e["topic"]) for e in quiz], [int(e["payload"]["correct"]) for e in quiz]))
    return seqs


def train_dkt_pipeline(epochs: int = 15) -> dict:
    from app.ml.dkt import train_dkt

    seqs = build_sequences()
    model, history = train_dkt(seqs[:24], num_topics=len(TOPICS), epochs=epochs)
    metrics = {"final_train_loss": float(history[-1]), "first_train_loss": float(history[0]),
               "students": len(seqs)}
    ModelRegistry("model_store").save_model("dkt", model, "1.0", metrics)
    print("DKT trained:", metrics)
    return metrics


if __name__ == "__main__":
    train_dkt_pipeline()
