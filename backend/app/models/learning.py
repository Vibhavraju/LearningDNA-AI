import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import DateTime, Float, ForeignKey, String, Text, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, UUIDMixin

if TYPE_CHECKING:
    from app.models.user import User

class MasteryState(Base):
    __tablename__ = "mastery_states"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    topic_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("topics.id"), primary_key=True)
    p_mastery: Mapped[float] = mapped_column(Float, default=0.0)
    p_init: Mapped[float] = mapped_column(Float, default=0.1)
    p_learn: Mapped[float] = mapped_column(Float, default=0.2)
    p_guess: Mapped[float] = mapped_column(Float, default=0.25)
    p_slip: Mapped[float] = mapped_column(Float, default=0.1)
    dkt_mastery: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user: Mapped["User"] = relationship(back_populates="mastery_states")

class RetentionParams(Base):
    __tablename__ = "retention_params"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    topic_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("topics.id"), primary_key=True)
    stability_days: Mapped[float] = mapped_column(Float, default=3.0)
    last_review_ts: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_perf: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    predicted_r: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

class DnaSnapshot(UUIDMixin, Base):
    __tablename__ = "dna_snapshots"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    speed: Mapped[float] = mapped_column(Float, default=0.0)
    retention: Mapped[float] = mapped_column(Float, default=0.0)
    attention: Mapped[float] = mapped_column(Float, default=0.0)
    quiz: Mapped[float] = mapped_column(Float, default=0.0)
    consistency: Mapped[float] = mapped_column(Float, default=0.0)
    overall: Mapped[float] = mapped_column(Float, default=0.0)
    traits: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    dna_vector: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    learner_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    narrative: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    user: Mapped["User"] = relationship(back_populates="dna_snapshots")
