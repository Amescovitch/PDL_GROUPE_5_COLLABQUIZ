from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, Table, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum
class SessionStatusEnum(enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    ENDED = "ended"

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True)
    host_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    code_pin = Column(String(20), unique=True, nullable=False, index=True)
    status = Column(Enum(SessionStatusEnum), default=SessionStatusEnum.PENDING, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ended_at = Column(DateTime, nullable=True)

    quiz = relationship("Quiz")
    host = relationship("User")