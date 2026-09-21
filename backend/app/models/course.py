from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False, index=True)
    degree_id = Column(Integer, ForeignKey("degrees.id", ondelete="SET NULL"), nullable=True, index=True)
    branch_id = Column(Integer, ForeignKey("branches.id", ondelete="SET NULL"), nullable=True, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="SET NULL"), nullable=True, index=True)
    
    title = Column(String(200), nullable=False, index=True)
    slug = Column(String(220), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=False)
    what_you_will_learn = Column(Text, nullable=True)  # JSON or newline-separated list
    requirements = Column(Text, nullable=True)
    instructor_name = Column(String(100), default="SkillSwap Campus Faculty")
    difficulty = Column(String(50), default="Beginner")  # Beginner, Intermediate, Advanced
    duration_hours = Column(Integer, default=10)
    thumbnail_url = Column(String(255), nullable=True)
    is_published = Column(Boolean, default=True)
    rating = Column(Float, default=4.8)
    enrollment_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    category = relationship("Category", back_populates="courses")
    degree = relationship("Degree", back_populates="courses")
    branch = relationship("Branch", back_populates="courses")
    skill = relationship("Skill", back_populates="courses")
    
    modules = relationship("CourseModule", back_populates="course", cascade="all, delete-orphan", order_by="CourseModule.order_index")
    enrollments = relationship("CourseEnrollment", back_populates="course", cascade="all, delete-orphan")
    final_assessment = relationship("FinalAssessment", back_populates="course", uselist=False, cascade="all, delete-orphan")
    certificates = relationship("Certificate", back_populates="course", cascade="all, delete-orphan")


class CourseModule(Base):
    __tablename__ = "course_modules"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    course = relationship("Course", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module", cascade="all, delete-orphan", order_by="Lesson.order_index")
    assessment = relationship("ModuleAssessment", back_populates="module", uselist=False, cascade="all, delete-orphan")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("course_modules.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    content_text = Column(Text, nullable=False)
    video_url = Column(String(255), nullable=True)
    resource_url = Column(String(255), nullable=True)
    duration_minutes = Column(Integer, default=15)
    order_index = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    module = relationship("CourseModule", back_populates="lessons")
    progress_records = relationship("LessonProgress", back_populates="lesson", cascade="all, delete-orphan")
