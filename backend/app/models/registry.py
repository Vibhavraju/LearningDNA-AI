from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, String, JSON, func
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, UUIDMixin

class ModelRegistry(UUIDMixin, Base):
    __tablename__ = "model_registry"
    name: Mapped[str] = mapped_column(String(255))
    version: Mapped[str] = mapped_column(String(50))
    path: Mapped[str] = mapped_column(String(500))
    metrics: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
