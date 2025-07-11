from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=True)
    google_id = Column(String, nullable=True)
    name = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    projects = relationship("Project", back_populates="user")
    ai_requests = relationship("AiRequest", back_populates="user")
    analytics = relationship("Analytics", back_populates="user")

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="active")
    data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="projects")

class AiRequest(Base):
    __tablename__ = "ai_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String, nullable=False)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="ai_requests")

class Analytics(Base):
    __tablename__ = "analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event = Column(String, nullable=False)
    data = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="analytics")
