from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True, default="BookOpen")

    degrees = relationship("Degree", back_populates="category", cascade="all, delete-orphan")
    courses = relationship("Course", back_populates="category")


class Degree(Base):
    __tablename__ = "degrees"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)

    category = relationship("Category", back_populates="degrees")
    branches = relationship("Branch", back_populates="degree", cascade="all, delete-orphan")
    users = relationship("User", back_populates="degree")
    courses = relationship("Course", back_populates="degree")


class Branch(Base):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True, index=True)
    degree_id = Column(Integer, ForeignKey("degrees.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(150), nullable=False)
    code = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)

    degree = relationship("Degree", back_populates="branches")
    users = relationship("User", back_populates="branch_rel")
    courses = relationship("Course", back_populates="branch")
