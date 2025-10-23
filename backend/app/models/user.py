""" from sqlalchemy import column, Integer,String, DateTime,Enum,Email


from backend.app.database import Base
class user(Base):
    __tablename__ = "users"
    id= column(Integer, primary_key=True)
    email= column(String,unique=True,nullable=False) """

# app/models/user.py
from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Enum, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

#from app.models import Attempt, Quiz, Session, SessionPlayer, Feedback, Notification, QuizVersion, Group, Badge
from .base import Base, UserRole

class User(Base):
    """
    Represents a registered user on the platform.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER, nullable=False)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )

    # Relationships
    quizzes: Mapped[List["Quiz"]] = relationship("Quiz", back_populates="author", cascade="all, delete-orphan")
    attempts: Mapped[List["Attempt"]] = relationship("Attempt", back_populates="user")
    hosted_sessions: Mapped[List["Session"]] = relationship("Session", back_populates="host")
    session_participations: Mapped[List["SessionPlayer"]] = relationship("SessionPlayer", back_populates="user")
    feedbacks: Mapped[List["Feedback"]] = relationship("Feedback", back_populates="user")
    notifications: Mapped[List["Notification"]] = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    quiz_versions: Mapped[List["QuizVersion"]] = relationship("QuizVersion", back_populates="editor")
    created_groups: Mapped[List["Group"]] = relationship("Group", back_populates="creator")
    
    # Many-to-many
    groups: Mapped[List["Group"]] = relationship(
        "Group", 
        secondary="user_groups", 
        back_populates="members"
    )
    badges: Mapped[List["Badge"]] = relationship(
        "Badge", 
        secondary="user_badges", 
        back_populates="users"
    )

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role={self.role})>"

