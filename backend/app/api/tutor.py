"""Tutor API: DNA-aware chat (JSON or SSE streaming) and history."""

from __future__ import annotations

import json
from collections.abc import Iterator

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from app.schemas import ChatRequest
from app.services.tutor_service import answer_question, stream_answer
from app.store import store

router = APIRouter(tags=["tutor"])


def _dna_summary(user_id: int) -> dict:
    dna = store.get_dna(user_id)
    return {"pace": dna["pace"], "preferred_format": dna["traits"]["preferred_format"],
            "attention": dna["attention_span_min"], "weak_topics": dna["weak_topics"]}


def _summary_for(user_id: int, request: ChatRequest) -> dict:
    """Prefer the profile supplied by the client; fall back to the stored DNA for this user."""
    if request.profile is not None:
        return {"pace": request.profile.pace, "preferred_format": request.profile.preferred_format,
                "attention": request.profile.attention, "weak_topics": request.profile.weak_topics}
    return _dna_summary(user_id)


@router.post("/tutor/chat")
def chat_with_tutor(user_id: int, request: ChatRequest, stream: bool = Query(False)):
    """Default: JSON {response, sources}. With ?stream=true: Server-Sent Events."""
    summary = _summary_for(user_id, request)
    store.add_message(user_id, "user", request.message)

    if not stream:
        answer, sources = answer_question(request.message, user_id, summary)
        store.add_message(user_id, "assistant", answer, sources)
        return {"user_id": user_id, "message": request.message, "response": answer, "sources": sources}

    chunks, sources = stream_answer(request.message, user_id, summary)

    def event_stream() -> Iterator[str]:
        parts: list[str] = []
        for chunk in chunks:
            parts.append(chunk)
            yield f"data: {json.dumps({'token': chunk})}\n\n"
        store.add_message(user_id, "assistant", "".join(parts), sources)
        yield f"data: {json.dumps({'done': True, 'sources': sources})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.get("/tutor/history")
def get_tutor_history(user_id: int, limit: int = Query(50, ge=1, le=500)):
    return {"user_id": user_id, "messages": store.user(user_id).tutor[-limit:]}
