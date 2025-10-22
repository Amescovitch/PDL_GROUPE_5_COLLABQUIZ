# app/models/question.py
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, Enum, Integer, String, Text, Float, ForeignKey, DateTime, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

#from app.models import Quiz, Attempt, SessionPlayer, User
from sqlalchemy.sql import func
from .base import Base, SessionStatus

class Session(Base):
    """
    Real-time game session based on a quiz.
    """
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True)
    host_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    pin_code: Mapped[str] = mapped_column(String(6), unique=True, nullable=False, index=True)
    status: Mapped[SessionStatus] = mapped_column(
        Enum(SessionStatus), 
        default=SessionStatus.WAITING, 
        nullable=False,
        index=True
    )
    current_question_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="sessions")
    host: Mapped["User"] = relationship("User", back_populates="hosted_sessions")
    players: Mapped[List["SessionPlayer"]] = relationship(
        "SessionPlayer", 
        back_populates="session", 
        cascade="all, delete-orphan"
    )
    attempts: Mapped[List["Attempt"]] = relationship("Attempt", back_populates="session")

    def __repr__(self):
        return f"<Session(id={self.id}, pin={self.pin_code}, status={self.status})>"


class SessionPlayer(Base):
    """
    Tracks players participating in a live session.
    Critical for real-time leaderboard and reconnection management.
    """
    __tablename__ = "session_players"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    pseudo: Mapped[str] = mapped_column(String(50), nullable=False)
    score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_connected: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    session: Mapped["Session"] = relationship("Session", back_populates="players")
    user: Mapped[Optional["User"]] = relationship("User", back_populates="session_participations")

    # Constraints
    __table_args__ = (
        UniqueConstraint('session_id', 'pseudo', name='uq_session_pseudo'),
        CheckConstraint('score >= 0', name='check_score_positive'),
    )

    def __repr__(self):
        return f"<SessionPlayer(id={self.id}, pseudo='{self.pseudo}', score={self.score})>"
