import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    semester = Column(Integer, nullable=False)
    branch = Column(String, nullable=False)

    registrations = relationship("Registration", back_populates="user")
    zen_metrics = relationship("ZenMetric", back_populates="user")


class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    type = Column(String, nullable=False) # e.g., Hackathon, Holiday, Exam
    date = Column(Date, nullable=False)
    tech_stack_tags = Column(String) # Comma-separated tags
    
    # CSV Specific fields
    college_name = Column(String) 
    location = Column(String)
    organizing_club = Column(String)

    registrations = relationship("Registration", back_populates="event")


class Registration(Base):
    __tablename__ = "registrations"

    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    event_id = Column(String, ForeignKey("events.id"), primary_key=True)
    registered_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="registrations")
    event = relationship("Event", back_populates="registrations")


class ZenMetric(Base):
    __tablename__ = "zen_metrics"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    session_length_minutes = Column(Integer, nullable=False)
    stress_level = Column(Integer, nullable=False) # 1-10
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="zen_metrics")
