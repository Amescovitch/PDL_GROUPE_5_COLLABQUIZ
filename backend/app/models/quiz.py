# app/models/quiz.py
from datetime import datetime
from typing import List, Optional
from sqlalchemy import JSON, CheckConstraint, Integer, String, Text, Boolean, DateTime, Enum, ARRAY, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
#from app.models import User, Question, Attempt, Session, Feedback
from .base import Base, QuizVisibility

class Quiz(Base):
    """
    A quiz is a collection of questions created by a user.
    """
    __tablename__ = "quizzes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    visibility: Mapped[QuizVisibility] = mapped_column(
        Enum(QuizVisibility), 
        default=QuizVisibility.PRIVATE, 
        nullable=False,
        index=True
    )
    tags: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )

    # Relationships
    author: Mapped["User"] = relationship("User", back_populates="quizzes")
    questions: Mapped[List["Question"]] = relationship(
        "Question", 
        back_populates="quiz", 
        cascade="all, delete-orphan",
        order_by="Question.order_index"
    )
    attempts: Mapped[List["Attempt"]] = relationship("Attempt", back_populates="quiz")
    sessions: Mapped[List["Session"]] = relationship("Session", back_populates="quiz")
    feedbacks: Mapped[List["Feedback"]] = relationship("Feedback", back_populates="quiz", cascade="all, delete-orphan")
    versions: Mapped[List["QuizVersion"]] = relationship("QuizVersion", back_populates="quiz", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Quiz(id={self.id}, title='{self.title}', visibility={self.visibility})>"

class QuizVersion(Base):
    """
    Manages successive versions of a quiz for collaborative editing.
    """
    __tablename__ = "quiz_versions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True)
    editor_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    changes: Mapped[dict] = mapped_column(JSON, nullable=False)  # JSON object with changes
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="versions")
    editor: Mapped["User"] = relationship("User", back_populates="quiz_versions")

    # Constraints
    __table_args__ = (
        UniqueConstraint('quiz_id', 'version', name='uq_quiz_version'),
        CheckConstraint('version > 0', name='check_version_positive'),
    )

    def __repr__(self):
        return f"<QuizVersion(id={self.id}, quiz_id={self.quiz_id}, version={self.version})>"
