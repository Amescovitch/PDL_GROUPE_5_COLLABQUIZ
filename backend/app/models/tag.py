from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, Table, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum
class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)

    quizzes = relationship("Quiz", secondary="quiz_tag", back_populates="tags")
