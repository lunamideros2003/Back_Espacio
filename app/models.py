from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(180), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    level: Mapped[str] = mapped_column(String(32), default="beginner")
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    city: Mapped[str | None] = mapped_column(String(120), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    attempts = relationship("QuizAttempt", back_populates="user")
    observations = relationship("Observation", back_populates="user")
    messages = relationship("ChatMessage", back_populates="user")


class CelestialObject(Base):
    __tablename__ = "celestial_objects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(160))
    type: Mapped[str] = mapped_column(String(40), index=True)
    constellation: Mapped[str | None] = mapped_column(String(80), nullable=True)
    magnitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    ra_hours: Mapped[float | None] = mapped_column(Float, nullable=True)
    dec_deg: Mapped[float | None] = mapped_column(Float, nullable=True)
    distance: Mapped[str | None] = mapped_column(String(160), nullable=True)
    diameter: Mapped[str | None] = mapped_column(String(160), nullable=True)
    fun_fact: Mapped[str] = mapped_column(Text)
    explain_beginner: Mapped[str] = mapped_column(Text)
    explain_medium: Mapped[str] = mapped_column(Text)
    explain_advanced: Mapped[str] = mapped_column(Text)
    image_query: Mapped[str] = mapped_column(String(160))
    tags: Mapped[str] = mapped_column(String(255))
    best_months: Mapped[str] = mapped_column(String(160))
    astronomy_body: Mapped[str | None] = mapped_column(String(40), nullable=True)

    observations = relationship("Observation", back_populates="object")
    questions = relationship("QuizQuestion", back_populates="object")


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    object_id: Mapped[int | None] = mapped_column(ForeignKey("celestial_objects.id"), nullable=True)
    level: Mapped[str] = mapped_column(String(32))
    question: Mapped[str] = mapped_column(Text)
    options: Mapped[str] = mapped_column(Text)
    correct_index: Mapped[int] = mapped_column(Integer)
    explanation: Mapped[str] = mapped_column(Text)

    object = relationship("CelestialObject", back_populates="questions")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    score: Mapped[int] = mapped_column(Integer)
    total: Mapped[int] = mapped_column(Integer)
    level: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="attempts")


class Observation(Base):
    __tablename__ = "observations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    object_id: Mapped[int] = mapped_column(ForeignKey("celestial_objects.id"))
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    visible: Mapped[bool] = mapped_column(Boolean, default=True)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="observations")
    object = relationship("CelestialObject", back_populates="observations")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    role: Mapped[str] = mapped_column(String(20))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="messages")
