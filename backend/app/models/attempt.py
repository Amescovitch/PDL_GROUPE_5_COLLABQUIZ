# app/models/attempt.py
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, Integer, Text, Float, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

#from app.models import Quiz, User, Session, Answer
from .base import Base

class Attempt(Base):
    """
    Represents a user's attempt to complete a quiz.
    """
    __tablename__ = "attempts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    session_id: Mapped[Optional[int]] = mapped_column(ForeignKey("sessions.id", ondelete="SET NULL"), nullable=True, index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    duration: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # seconds
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="attempts")
    user: Mapped[Optional["User"]] = relationship("User", back_populates="attempts")
    session: Mapped[Optional["Session"]] = relationship("Session", back_populates="attempts")
    answers: Mapped[List["Answer"]] = relationship("Answer", back_populates="attempt", cascade="all, delete-orphan")

    # Constraints
    __table_args__ = (
        CheckConstraint('score IS NULL OR (score >= 0 AND score <= 100)', name='check_score_range'),
        CheckConstraint('duration IS NULL OR duration >= 0', name='check_duration_positive'),
    )

    def __repr__(self):
        return f"<Attempt(id={self.id}, quiz_id={self.quiz_id}, score={self.score})>"
