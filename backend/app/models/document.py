import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import JSON as _JSON
from app.config import get_database_url

_EmbeddingType = _JSON  # SQLite / fallback
if get_database_url().startswith("postgresql"):
    try:  # pgvector column only makes sense on PostgreSQL
        from pgvector.sqlalchemy import Vector

        _EmbeddingType = Vector(384)
    except ImportError:  # pragma: no cover
        pass
from app.models.base import Base, UUIDMixin

if TYPE_CHECKING:
    from app.models.user import User

class Document(UUIDMixin, Base):
    __tablename__ = "documents"
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(500))
    source: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="processing")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    owner: Mapped["User"] = relationship(back_populates="documents")
    chunks: Mapped[list["Chunk"]] = relationship(back_populates="document", cascade="all, delete-orphan")

class Chunk(UUIDMixin, Base):
    __tablename__ = "chunks"
    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("documents.id"))
    topic_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("topics.id"), nullable=True)
    text: Mapped[str] = mapped_column(Text)
    embedding = mapped_column(_EmbeddingType, nullable=True)
    document: Mapped["Document"] = relationship(back_populates="chunks")
