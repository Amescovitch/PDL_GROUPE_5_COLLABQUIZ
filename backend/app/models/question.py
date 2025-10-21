from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, Table, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum
class QuestionTypeEnum(enum.Enum):
    MCQ = "MCQ"
    TF = "TF"
    SHORT = "SHORT"

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True)
    text = Column(Text, nullable=False)
    type = Column(Enum(QuestionTypeEnum), default=QuestionTypeEnum.MCQ, nullable=False)
    time_limit_sec = Column(Integer, nullable=True)
    weight = Column(Float, default=1.0, nullable=False)

    quiz = relationship("Quiz", back_populates="questions")
    choices = relationship("Choice", back_populates="question", cascade="all, delete-orphan")
    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")
