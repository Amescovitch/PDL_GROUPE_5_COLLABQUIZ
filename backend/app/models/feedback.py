# app/models/question.py
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, Integer, Text, Float, ForeignKey, DateTime, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

#from app.models import Quiz, User
from .base import Base

class Feedback(Base):
    """
    Allows users to rate and comment on quizzes.
    """
    __tablename__ = "feedbacks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="feedbacks")
    user: Mapped["User"] = relationship("User", back_populates="feedbacks")

    # Constraints
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
        UniqueConstraint('quiz_id', 'user_id', name='uq_quiz_user_feedback'),
    )

    def __repr__(self):
        return f"<Feedback(id={self.id}, rating={self.rating})>"
