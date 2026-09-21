from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    certificate_id = Column(String(64), unique=True, nullable=False, index=True)  # e.g. SSC-PY-2026-000123
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    issue_date = Column(DateTime(timezone=True), server_default=func.now())
    student_name = Column(String(150), nullable=False)
    course_title = Column(String(200), nullable=False)
    grade = Column(String(50), default="Distinction")
    verification_url = Column(String(255), nullable=False)
    pdf_path = Column(String(255), nullable=True)

    user = relationship("User", back_populates="certificates")
    course = relationship("Course", back_populates="certificates")
