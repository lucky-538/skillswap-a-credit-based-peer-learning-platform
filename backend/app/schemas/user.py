from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, ConfigDict

from app.schemas.academic import DegreeResponse, BranchResponse
from app.schemas.skill import SkillTeachResponse, SkillLearnResponse


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    college: Optional[str] = None
    degree_id: Optional[int] = None
    branch_id: Optional[int] = None
    branch: Optional[str] = None
    year: Optional[int] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    college: Optional[str] = None
    degree_id: Optional[int] = None
    branch_id: Optional[int] = None
    branch: Optional[str] = None
    year: Optional[int] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    college: Optional[str] = None
    branch: Optional[str] = None
    year: Optional[int] = None
    degree_id: Optional[int] = None
    branch_id: Optional[int] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    credits: int = 10
    reputation_score: float = 5.0
    is_active: bool = True
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class UserProfileResponse(UserResponse):
    degree: Optional[DegreeResponse] = None
    branch_rel: Optional[BranchResponse] = None
    skills_teach: List[SkillTeachResponse] = []
    skills_learn: List[SkillLearnResponse] = []
    courses_enrolled_count: int = 0
    courses_completed_count: int = 0
    certificates_count: int = 0
    swaps_completed_count: int = 0
    average_rating: float = 5.0
    review_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class PublicUserResponse(BaseModel):
    id: int
    name: str
    college: Optional[str] = None
    branch: Optional[str] = None
    year: Optional[int] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    reputation_score: float = 5.0
    skills_teach: List[SkillTeachResponse] = []
    skills_learn: List[SkillLearnResponse] = []
    swaps_completed_count: int = 0
    average_rating: float = 5.0
    review_count: int = 0

    model_config = ConfigDict(from_attributes=True)