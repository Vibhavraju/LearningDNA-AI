"""Tutor service: DNA-aware personalised tutoring using RAG + LLM."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from app.services.llm import get_llm_provider
from app.services.rag import retrieve_chunks


def build_tutor_prompt(question: str, dna_summary: dict[str, Any], retrieved_chunks: list[dict[str, Any]]) -> tuple[str, str]:
    context = "\n\n".join(f"- {c['text']} (source: {c['document_title']})" for c in retrieved_chunks)
    system_prompt = f"""You are a personalised AI tutor for Learning DNA AI.

Student Profile:
- Learning Pace: {dna_summary.get('pace', 'Moderate')}
- Preferred Format: {dna_summary.get('preferred_format', 'Visual + Practice')}
- Attention Span: {dna_summary.get('attention', 40)} minutes
- Weak Topics: {', '.join(dna_summary.get('weak_topics', [])) or 'none identified yet'}

Teaching Guidelines:
- Adapt the explanation style to the student's pace and format preference
- Keep explanations concise if the attention span is low
- Revisit prerequisites when the question touches a weak topic
- Use the provided context to ground your answer and cite document sources
- If the context does not cover the question, say so honestly

Context:
{context}
"""
    return system_prompt, question


def retrieve_for(question: str, user_id: int) -> list[dict[str, Any]]:
    return retrieve_chunks(question, owner=user_id, top_k=3)


def answer_question(question: str, user_id: int, dna_summary: dict[str, Any]) -> tuple[str, list[str]]:
    chunks = retrieve_for(question, user_id)
    system_prompt, user_message = build_tutor_prompt(question, dna_summary, chunks)
    answer = get_llm_provider().generate(system_prompt, user_message)
    return answer, sorted({c["document_title"] for c in chunks})


def stream_answer(question: str, user_id: int, dna_summary: dict[str, Any]) -> tuple[Iterator[str], list[str]]:
    chunks = retrieve_for(question, user_id)
    system_prompt, user_message = build_tutor_prompt(question, dna_summary, chunks)
    return get_llm_provider().stream(system_prompt, user_message), sorted({c["document_title"] for c in chunks})
