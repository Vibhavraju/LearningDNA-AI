from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class EventCreate(BaseModel):
    user_id: int
    ts: datetime
    type: str  # session | quiz_answer | content_view
    topic: Optional[str] = None
    payload: dict[str, Any] = Field(default_factory=dict)


class TutorProfile(BaseModel):
    """Optional learner context sent by the client so answers match the learner's own DNA."""

    pace: str = "Moderate"
    preferred_format: str = "Visual + Practice"
    attention: float = Field(default=40, ge=0, le=240)
    weak_topics: list[str] = Field(default_factory=list, max_length=10)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    topic_id: Optional[int] = None
    profile: Optional[TutorProfile] = None


class SettingsUpdate(BaseModel):
    dna_weights: Optional[dict[str, float]] = None
    daily_minutes: Optional[int] = Field(default=None, ge=10, le=600)
    llm_provider: Optional[str] = None
    mastery_model: Optional[str] = None
    theme: Optional[str] = None
