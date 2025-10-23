# app/models/question.py
from datetime import datetime
from typing import List, Optional
from click import Choice
from sqlalchemy import Boolean, Integer, Text, Float, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

#from app.models import Attempt, Question
from .base import Base

class Answer(Base):
    """
    Answer given by a user to a question during an attempt.
    """
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    attempt_id: Mapped[int] = mapped_column(ForeignKey("attempts.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    chosen_choice_id: Mapped[Optional[int]] = mapped_column(ForeignKey("choices.id", ondelete="SET NULL"), nullable=True)
    text_answer: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    time_taken: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # milliseconds
    answered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    attempt: Mapped["Attempt"] = relationship("Attempt", back_populates="answers")
    question: Mapped["Question"] = relationship("Question", back_populates="answers")
    chosen_choice: Mapped[Optional["Choice"]] = relationship("Choice", back_populates="answers")

    # Constraints
    __table_args__ = (
        CheckConstraint('time_taken IS NULL OR time_taken >= 0', name='check_time_taken_positive'),
    )

    def __repr__(self):
        return f"<Answer(id={self.id}, is_correct={self.is_correct})>"
