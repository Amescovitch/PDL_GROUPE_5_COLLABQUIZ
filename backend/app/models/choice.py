# app/models/choice.py
from datetime import datetime
from typing import List, Optional
from sqlalchemy import JSON, Boolean, Integer, String, Text, Float, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

#from app.models import Answer, Question
from .base import Base

class Choice(Base):
    """
    Represents a possible choice for a question (MCQ/True-False).
    """
    __tablename__ = "choices"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    text: Mapped[str] = mapped_column(String(500), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    question: Mapped["Question"] = relationship("Question", back_populates="choices")
    answers: Mapped[List["Answer"]] = relationship("Answer", back_populates="chosen_choice")

    def __repr__(self):
        return f"<Choice(id={self.id}, is_correct={self.is_correct})>"



