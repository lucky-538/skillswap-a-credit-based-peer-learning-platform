from typing import List, Optional
from pydantic import BaseModel


class AdminStatsResponse(BaseModel):
    total_students: int
    total_courses: int
    total_enrollments: int
    total_skill_swaps: int
    completed_courses: int
    certificates_issued: int
    total_skills: int
    total_categories: int


class UserStatusUpdate(BaseModel):
    is_active: bool
    role: Optional[str] = None
