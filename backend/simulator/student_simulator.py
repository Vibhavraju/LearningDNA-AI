"""CLI wrapper around the event simulator."""
from app.simulation import PERSONAS, generate_events  # noqa: F401

if __name__ == "__main__":
    for p in PERSONAS:
        evs = generate_events(p, days=28)
        quiz = [e for e in evs if e["type"] == "quiz_answer"]
        acc = sum(e["payload"]["correct"] for e in quiz) / max(len(quiz), 1)
        print(f"{p.name}: {len(evs)} events, {len(quiz)} quiz answers, accuracy {acc:.0%}")
