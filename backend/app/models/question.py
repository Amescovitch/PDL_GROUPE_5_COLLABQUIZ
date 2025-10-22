# app/models/question.py
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Enum, Integer, Text, Float, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sqlalchemy.sql import func

#from app.models import Answer, Choice, Quiz
from .base import Base, QuestionType

class Question(Base):
    """
    A question belongs to a quiz and can be MCQ, True/False, or Short Answer.
    """
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True)
    type: Mapped[QuestionType] = mapped_column(Enum(QuestionType), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    time_limit_sec: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    weight: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="questions")
    choices: Mapped[List["Choice"]] = relationship(
        "Choice", 
        back_populates="question", 
        cascade="all, delete-orphan",
        order_by="Choice.order_index"
    )
    answers: Mapped[List["Answer"]] = relationship("Answer", back_populates="question")

    # Constraints
    __table_args__ = (
        CheckConstraint('time_limit_sec IS NULL OR time_limit_sec > 0', name='check_time_limit_positive'),
        CheckConstraint('weight > 0', name='check_weight_positive'),
    )

    def __repr__(self):
        return f"<Question(id={self.id}, type={self.type}, quiz_id={self.quiz_id})>"
