"""DNA API: profile, traits, history, explanation, recompute."""

from __future__ import annotations

from fastapi import APIRouter

from app.api.ws import manager
from app.services.explain import explain_snapshots
from app.services.narrative import generate_learning_analysis
from app.store import store

router = APIRouter(tags=["dna"])


def _profile(dna: dict) -> dict:
    return {
        "user_id": dna["user_id"],
        "overall": dna["overall"],
        "confidence": dna["confidence"],
        "dimensions": {
            "learning_speed": dna["speed"], "knowledge_retention": dna["retention"],
            "attention_span": dna["attention"], "quiz_performance": dna["quiz"],
            "learning_consistency": dna["consistency"],
        },
        # flat copies for simple clients
        "speed": dna["speed"], "retention": dna["retention"], "attention": dna["attention"],
        "quiz": dna["quiz"], "consistency": dna["consistency"],
        "learner_type": dna["learner_type"], "pace": dna["pace"],
        "weak_topics": dna["weak_topics"], "strong_topics": dna["strong_topics"],
        "narrative": generate_learning_analysis(dna),
    }


@router.get("/dna/{user_id}")
def get_dna(user_id: int):
    return _profile(store.get_dna(user_id))


@router.get("/dna/{user_id}/traits")
def get_traits(user_id: int):
    dna = store.get_dna(user_id)
    return {"learner_type": dna["learner_type"], "characteristics": dna["traits"], **dna["traits"],
            "attention_span_min": dna["attention_span_min"]}


@router.get("/dna/{user_id}/history")
def get_dna_history(user_id: int):
    store.get_dna(user_id)
    return [{"week": s.get("week", i + 1), "speed": s["speed"], "retention": s["retention"],
             "attention": s["attention"], "quiz": s["quiz"], "consistency": s["consistency"],
             "overall": s["overall"]} for i, s in enumerate(store.user(user_id).snapshots)]


@router.get("/dna/{user_id}/explain")
def explain_dna(user_id: int):
    store.get_dna(user_id)
    snaps = store.user(user_id).snapshots
    new = store.get_dna(user_id)
    old = snaps[-2] if len(snaps) >= 2 else None
    return explain_snapshots(old, new)


@router.post("/dna/{user_id}/recompute")
async def recompute_dna(user_id: int):
    dna = store.recompute_dna(user_id)
    profile = _profile(dna)
    await manager.broadcast_dna_update(user_id, profile)
    return {"status": "recomputed", **profile}
