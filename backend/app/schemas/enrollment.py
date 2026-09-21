from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from app.schemas.course import CourseResponse, LessonResponse


class EnrollmentResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    enrolled_at: Optional[datetime] = None
    progress_percentage: float = 0.0
    status: str  # enrolled, in-progress, completed
    completed_at: Optional[datetime] = None
    course: CourseResponse

    model_config = ConfigDict(from_attributes=True)


class LearningLesson(BaseModel):
    id: int
    module_id: int
    title: str
    description: Optional[str] = None
    content_text: str
    video_url: Optional[str] = None
    resource_url: Optional[str] = None
    duration_minutes: int
    order_index: int
    is_completed: bool = False

    model_config = ConfigDict(from_attributes=True)


class LearningModule(BaseModel):
    id: int
    course_id: int
    title: str
    description: Optional[str] = None
    order_index: int
    is_unlocked: bool = True
    is_completed: bool = False
    lessons_completed_count: int = 0
    total_lessons_count: int = 0
    assessment_id: Optional[int] = None
    assessment_passed: bool = False
    assessment_score: Optional[float] = None
    lessons: List[LearningLesson] = []

    model_config = ConfigDict(from_attributes=True)


class LearningCourseView(BaseModel):
    course: CourseResponse
    enrollment: EnrollmentResponse
    modules: List[LearningModule] = []
    final_assessment_unlocked: bool = False
    final_assessment_passed: bool = False
    certificate_id: Optional[str] = None
