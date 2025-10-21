from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, Table, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum
# Association tables
quiz_tag_table = Table(
    "quiz_tag",
    Base.metadata,
    Column("quiz_id", Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)

quiz_group_table = Table(
    "quiz_group",
    Base.metadata,
    Column("quiz_id", Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), primary_key=True),
    Column("group_id", Integer, ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True),
)

class VisibilityEnum(enum.Enum):
    PRIVATE = "private"
    GROUP = "group"
    PUBLIC = "public"

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    visibility = Column(Enum(VisibilityEnum), default=VisibilityEnum.PRIVATE, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    author = relationship("User", back_populates="quizzes")
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
    attempts = relationship("Attempt", back_populates="quiz", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary=quiz_tag_table, back_populates="quizzes")
    groups = relationship("Group", secondary=quiz_group_table, back_populates="quizzes")
    versions = relationship("QuizVersion", back_populates="quiz", cascade="all, delete-orphan")
    feedbacks = relationship("Feedback", back_populates="quiz", cascade="all, delete-orphan")
