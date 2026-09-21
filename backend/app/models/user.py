from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="student")  # student, admin
    college = Column(String(150), nullable=True)
    branch = Column(String(100), nullable=True)  # textual fallback
    year = Column(Integer, nullable=True)
    
    degree_id = Column(Integer, ForeignKey("degrees.id", ondelete="SET NULL"), nullable=True)
    branch_id = Column(Integer, ForeignKey("branches.id", ondelete="SET NULL"), nullable=True)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    credits = Column(Integer, default=10)
    reputation_score = Column(Float, default=5.0)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    degree = relationship("Degree", foreign_keys=[degree_id], back_populates="users")
    branch_rel = relationship("Branch", foreign_keys=[branch_id], back_populates="users")
    
    skills_teach = relationship("UserSkillTeach", back_populates="user", cascade="all, delete-orphan")
    skills_learn = relationship("UserSkillLearn", back_populates="user", cascade="all, delete-orphan")
    
    sent_swap_requests = relationship("SkillSwapRequest", foreign_keys="SkillSwapRequest.sender_id", back_populates="sender", cascade="all, delete-orphan")
    received_swap_requests = relationship("SkillSwapRequest", foreign_keys="SkillSwapRequest.receiver_id", back_populates="receiver", cascade="all, delete-orphan")
    
    enrollments = relationship("CourseEnrollment", back_populates="user", cascade="all, delete-orphan")
    certificates = relationship("Certificate", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    
    reviews_given = relationship("Review", foreign_keys="Review.reviewer_id", back_populates="reviewer", cascade="all, delete-orphan")
    reviews_received = relationship("Review", foreign_keys="Review.reviewee_id", back_populates="reviewee", cascade="all, delete-orphan")