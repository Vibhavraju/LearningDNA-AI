import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, JSON, Boolean, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, UUIDMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.content import QuizQuestion

class Event(UUIDMixin, Base):
    __tablename__ = "events"
    __table_args__ = (Index("ix_events_user_ts", "user_id", "ts"),)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    type: Mapped[str] = mapped_column(String(50))
    topic_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("topics.id"), nullable=True)
    content_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("content_items.id"), nullable=True)
    session_id: Mapped[Optional[uuid.UUID]] = mapped_column(nullable=True)
    payload: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    user: Mapped["User"] = relationship(back_populates="events")

class Session(UUIDMixin, Base):
    __tablename__ = "sessions"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    start_ts: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_ts: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_min: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    subject_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("subjects.id"), nullable=True)
    user: Mapped["User"] = relationship(back_populates="sessions")

class QuizAttempt(UUIDMixin, Base):
    __tablename__ = "quiz_attempts"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    question_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("quiz_questions.id"))
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    correct: Mapped[bool] = mapped_column(Boolean)
    response_time_s: Mapped[float] = mapped_column(Float)
    attempt_no: Mapped[int] = mapped_column(Integer, default=1)
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    user: Mapped["User"] = relationship(back_populates="quiz_attempts")
    question: Mapped["QuizQuestion"] = relationship(back_populates="attempts")
