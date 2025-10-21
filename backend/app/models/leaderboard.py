from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, Table, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum
class Leaderboard(Base):
    __tablename__ = "leaderboard"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    total_points = Column(Integer, default=0, nullable=False)
    rank = Column(Integer, nullable=True)

    user = relationship("User")
