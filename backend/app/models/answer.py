from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, Table, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base
import enum
class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("attempts.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    chosen_choice_id = Column(Integer, ForeignKey("choices.id", ondelete="SET NULL"), nullable=True)
    text_answer = Column(Text, nullable=True)
    correct = Column(Boolean, nullable=True)

    attempt = relationship("Attempt", back_populates="answers")
    question = relationship("Question", back_populates="answers")
