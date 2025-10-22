# app/models/notification.py
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, Integer, String, Text, Float, ForeignKey, DateTime, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

#from app.models import User
from .base import Base

class Notification(Base):
    """
    System notifications for users.
    """
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification(id={self.id}, type='{self.type}', is_read={self.is_read})>"
