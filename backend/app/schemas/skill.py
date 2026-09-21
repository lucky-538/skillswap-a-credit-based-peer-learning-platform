from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class SkillBase(BaseModel):
    name: str
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    description: Optional[str] = None


class SkillCreate(SkillBase):
    pass


class SkillResponse(SkillBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class SkillTeachCreate(BaseModel):
    skill_id: Optional[int] = None
    skill_name: Optional[str] = None  # in case user enters a new skill name
    category_name: Optional[str] = None
    proficiency_level: str = "Intermediate"  # Beginner, Intermediate, Advanced, Expert
    experience_description: Optional[str] = None


class SkillTeachResponse(BaseModel):
    id: int
    user_id: int
    skill_id: int
    skill: SkillResponse
    proficiency_level: str
    experience_description: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class SkillLearnCreate(BaseModel):
    skill_id: Optional[int] = None
    skill_name: Optional[str] = None
    category_name: Optional[str] = None
    desired_level: str = "Beginner"  # Beginner, Intermediate, Advanced
    notes: Optional[str] = None


class SkillLearnResponse(BaseModel):
    id: int
    user_id: int
    skill_id: int
    skill: SkillResponse
    desired_level: str
    notes: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
