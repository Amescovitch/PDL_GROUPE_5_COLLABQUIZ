# app/models/group.py
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Enum, Boolean, Integer, String, Text, Float, ForeignKey, DateTime, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

#from app.models import User
from .base import Base, GroupRole

class Group(Base):
    """
    Represents a group of users for sharing and collaboration.
    """
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    invite_code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, index=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    creator: Mapped["User"] = relationship("User", back_populates="created_groups")
    members: Mapped[List["User"]] = relationship(
        "User", 
        secondary="user_groups", 
        back_populates="groups"
    )

    def __repr__(self):
        return f"<Group(id={self.id}, name='{self.name}')>"


class UserGroup(Base):
    """
    Association table: User <-> Group with role.
    """
    __tablename__ = "user_groups"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True)
    role: Mapped[GroupRole] = mapped_column(Enum(GroupRole), default=GroupRole.MEMBER, nullable=False)
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<UserGroup(user_id={self.user_id}, group_id={self.group_id}, role={self.role})>"
