"""Human-readable text generated from DNA data."""

from __future__ import annotations

from typing import Any


def generate_learning_analysis(dna: dict[str, Any]) -> str:
    traits = dna.get("traits", {})
    strong = (dna.get("strong_topics") or ["your strongest topics"])[0]
    gap = (dna.get("weak_topics") or ["no clear gap yet"])[0]
    pace = str(dna.get("pace", traits.get("learning_pace", "Moderate"))).lower()
    fmt = traits.get("preferred_format", "Visual explanations followed by hands-on problems")
    return (
        f"Your strongest performance is in {strong}. "
        f"You learn at a {pace} pace. "
        f"Retention drops when concepts are not revised within {max(2, round(dna.get('features', {}).get('mean_stability_days', 3)))} days. "
        f"Your largest knowledge gap is {gap}. "
        f"{fmt} material works best for you. "
        "Recommended strategy: learn -> visual explanation -> 3 easy problems -> 2 medium problems -> revise after 3 days."
    )


def generate_update_message(old_dna: dict[str, Any], new_dna: dict[str, Any]) -> str:
    def delta(key: str) -> int:
        return int(round(new_dna.get(key, 0) - old_dna.get(key, 0)))

    r, q = delta("retention"), delta("quiz")
    return (f"Your Learning DNA has been updated. Retention {'improved' if r >= 0 else 'declined'} by {abs(r)} "
            f"and quiz performance {'improved' if q >= 0 else 'declined'} by {abs(q)} points "
            "compared with the previous assessment.")


def generate_learner_identity_text(dna: dict[str, Any]) -> str:
    traits = dna.get("traits", {})
    return f"""
YOUR LEARNING DNA - IDENTITY CARD

Learner Type:      {dna.get('learner_type', 'Unknown')}
Learning Pace:     {dna.get('pace', 'n/a')}
Retention:         {dna.get('retention', 0)}/100
Consistency:       {dna.get('consistency_label', 'n/a')}
Attention Span:    {dna.get('attention_span_min', 0)} minutes
Best Study Time:   {traits.get('best_study_time', 'n/a')}
DNA Confidence:    {dna.get('confidence', 0)}%

Strengths:  {', '.join(dna.get('strong_topics', [])) or 'n/a'}
Improve:    {', '.join(dna.get('weak_topics', [])) or 'n/a'}
"""
