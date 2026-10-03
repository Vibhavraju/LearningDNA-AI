import uuid
from typing import TYPE_CHECKING, Optional
from sqlalchemy import ForeignKey, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User

class UserSettings(Base):
    __tablename__ = "user_settings"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    dna_weights: Mapped[Optional[dict]] = mapped_column(JSON, default=lambda: {"speed": 0.25, "retention": 0.30, "attention": 0.10, "quiz": 0.15, "consistency": 0.20})
    llm_provider: Mapped[Optional[str]] = mapped_column(String(50), default="mock")
    mastery_model: Mapped[Optional[str]] = mapped_column(String(50), default="bkt")
    daily_minutes: Mapped[int] = mapped_column(Integer, default=90)
    theme: Mapped[Optional[str]] = mapped_column(String(50), default="light")
    user: Mapped["User"] = relationship()
