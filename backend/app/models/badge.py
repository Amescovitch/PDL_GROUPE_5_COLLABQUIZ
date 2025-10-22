# app/models/badge.py
from datetime import datetime
from typing import List, Optional
from sqlalchemy import JSON, Integer, String, Text, Float, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

#from app.models import User
from .base import Base

class Badge(Base):
    """
    Achievement badges that can be earned by users (gamification).
    """
    __tablename__ = "badges"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    icon_url: Mapped[str] = mapped_column(String(500), nullable=False)
    criteria: Mapped[dict] = mapped_column(JSON, nullable=False)  # Conditions to earn badge

    # Relationships
    users: Mapped[List["User"]] = relationship(
        "User", 
        secondary="user_badges", 
        back_populates="badges"
    )

    def __repr__(self):
        return f"<Badge(id={self.id}, name='{self.name}')>"


class UserBadge(Base):
    """
    Association table: User <-> Badge with earned date.
    """
    __tablename__ = "user_badges"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    badge_id: Mapped[int] = mapped_column(ForeignKey("badges.id", ondelete="CASCADE"), primary_key=True)
    earned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<UserBadge(user_id={self.user_id}, badge_id={self.badge_id})>"