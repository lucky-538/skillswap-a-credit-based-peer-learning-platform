from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from app.schemas.academic import CategoryResponse, DegreeResponse, BranchResponse
from app.schemas.skill import SkillResponse


class LessonBase(BaseModel):
    title: str
    description: Optional[str] = None
    content_text: str
    video_url: Optional[str] = None
    resource_url: Optional[str] = None
    duration_minutes: int = 15
    order_index: int = 1


class LessonCreate(LessonBase):
    module_id: int


class LessonResponse(LessonBase):
    id: int
    module_id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ModuleBase(BaseModel):
    title: str
    description: Optional[str] = None
    order_index: int = 1


class ModuleCreate(ModuleBase):
    course_id: int


class ModuleResponse(ModuleBase):
    id: int
    course_id: int
    lessons: List[LessonResponse] = []
    has_assessment: bool = False
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CourseBase(BaseModel):
    title: str
    category_id: int
    degree_id: Optional[int] = None
    branch_id: Optional[int] = None
    skill_id: Optional[int] = None
    description: str
    what_you_will_learn: Optional[str] = None
    requirements: Optional[str] = None
    instructor_name: Optional[str] = "SkillSwap Campus Faculty"
    difficulty: str = "Beginner"  # Beginner, Intermediate, Advanced
    duration_hours: int = 10
    thumbnail_url: Optional[str] = None
    is_published: bool = True


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    category_id: Optional[int] = None
    degree_id: Optional[int] = None
    branch_id: Optional[int] = None
    skill_id: Optional[int] = None
    description: Optional[str] = None
    what_you_will_learn: Optional[str] = None
    requirements: Optional[str] = None
    instructor_name: Optional[str] = None
    difficulty: Optional[str] = None
    duration_hours: Optional[int] = None
    thumbnail_url: Optional[str] = None
    is_published: Optional[bool] = None


class CourseResponse(CourseBase):
    id: int
    slug: str
    rating: float = 4.8
    enrollment_count: int = 0
    modules_count: int = 0
    category: Optional[CategoryResponse] = None
    degree: Optional[DegreeResponse] = None
    branch: Optional[BranchResponse] = None
    skill: Optional[SkillResponse] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CourseDetailResponse(CourseResponse):
    modules: List[ModuleResponse] = []
    has_final_assessment: bool = False
    certificate_available: bool = True

    model_config = ConfigDict(from_attributes=True)
