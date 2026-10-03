import uuid
from typing import TYPE_CHECKING, Optional
from sqlalchemy import Float, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, UUIDMixin

if TYPE_CHECKING:
    from app.models.activity import QuizAttempt

class Subject(UUIDMixin, Base):
    __tablename__ = "subjects"
    name: Mapped[str] = mapped_column(String(255), unique=True)
    topics: Mapped[list["Topic"]] = relationship(back_populates="subject", cascade="all, delete-orphan")

class Topic(UUIDMixin, Base):
    __tablename__ = "topics"
    subject_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("subjects.id"))
    name: Mapped[str] = mapped_column(String(255))
    difficulty: Mapped[float] = mapped_column(Float, default=0.5)
    order: Mapped[int] = mapped_column(Integer, default=0)
    subject: Mapped["Subject"] = relationship(back_populates="topics")
    prerequisites: Mapped[list["TopicPrerequisite"]] = relationship(
        foreign_keys="TopicPrerequisite.topic_id", back_populates="topic", cascade="all, delete-orphan"
    )
    content_items: Mapped[list["ContentItem"]] = relationship(back_populates="topic", cascade="all, delete-orphan")
    quiz_questions: Mapped[list["QuizQuestion"]] = relationship(back_populates="topic", cascade="all, delete-orphan")

class TopicPrerequisite(Base):
    __tablename__ = "topic_prerequisites"
    topic_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("topics.id"), primary_key=True)
    prereq_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("topics.id"), primary_key=True)
    weight: Mapped[float] = mapped_column(Float, default=1.0)
    topic: Mapped["Topic"] = relationship(foreign_keys=[topic_id], back_populates="prerequisites")
    prereq: Mapped["Topic"] = relationship(foreign_keys=[prereq_id])

class ContentItem(UUIDMixin, Base):
    __tablename__ = "content_items"
    topic_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("topics.id"))
    type: Mapped[str] = mapped_column(String(50))
    title: Mapped[str] = mapped_column(String(500))
    duration_min: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    topic: Mapped["Topic"] = relationship(back_populates="content_items")

class QuizQuestion(UUIDMixin, Base):
    __tablename__ = "quiz_questions"
    topic_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("topics.id"))
    difficulty: Mapped[float] = mapped_column(Float, default=0.5)
    text: Mapped[str] = mapped_column(String)
    options: Mapped[dict] = mapped_column(JSON)
    correct_idx: Mapped[int] = mapped_column(Integer)
    explanation: Mapped[str] = mapped_column(String, default="")
    topic: Mapped["Topic"] = relationship(back_populates="quiz_questions")
    attempts: Mapped[list["QuizAttempt"]] = relationship(back_populates="question", cascade="all, delete-orphan")
