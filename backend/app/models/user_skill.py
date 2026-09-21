from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class UserSkillTeach(Base):
    __tablename__ = "user_skills_teach"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    proficiency_level = Column(String(50), nullable=False, default="Intermediate")  # Beginner, Intermediate, Advanced, Expert
    experience_description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="skills_teach")
    skill = relationship("Skill", back_populates="teachers")


class UserSkillLearn(Base):
    __tablename__ = "user_skills_learn"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    desired_level = Column(String(50), nullable=False, default="Beginner")  # Beginner, Intermediate, Advanced
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="skills_learn")
    skill = relationship("Skill", back_populates="learners")
