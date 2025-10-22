# app/models/base.py
from sqlalchemy.orm import DeclarativeBase
import enum

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass

class UserRole(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class QuizVisibility(str, enum.Enum):
    PRIVATE = "PRIVATE"
    SHARED = "SHARED"
    PUBLIC = "PUBLIC"

class QuestionType(str, enum.Enum):
    MCQ = "MCQ"
    TF = "TF"
    SHORT = "SHORT"

class SessionStatus(str, enum.Enum):
    WAITING = "WAITING"
    ACTIVE = "ACTIVE"
    FINISHED = "FINISHED"

class GroupRole(str, enum.Enum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"
