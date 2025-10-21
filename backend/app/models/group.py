from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, Table, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum
class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    users = relationship("UserGroup", back_populates="group", cascade="all, delete-orphan")
    quizzes = relationship("Quiz", secondary="quiz_group", back_populates="groups")

class UserGroup(Base):
    __tablename__ = "user_group"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True)

    user = relationship("User", back_populates="groups")
    group = relationship("Group", back_populates="users")
