from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class OptionBase(BaseModel):
    option_text: str
    is_correct: bool = False


class OptionCreate(OptionBase):
    pass


class OptionResponse(BaseModel):
    id: int
    question_id: int
    option_text: str

    model_config = ConfigDict(from_attributes=True)


class QuestionBase(BaseModel):
    question_text: str
    explanation: Optional[str] = None
    marks: int = 1
    order_index: int = 1


class QuestionCreate(QuestionBase):
    options: List[OptionCreate]


class QuestionResponse(BaseModel):
    id: int
    assessment_id: int
    question_text: str
    marks: int
    order_index: int
    options: List[OptionResponse]

    model_config = ConfigDict(from_attributes=True)


class ModuleAssessmentCreate(BaseModel):
    module_id: int
    title: str
    description: Optional[str] = None
    passing_percentage: float = 70.0
    time_limit_minutes: int = 15
    questions: List[QuestionCreate] = []


class ModuleAssessmentDetail(BaseModel):
    id: int
    module_id: int
    module_title: Optional[str] = None
    course_id: Optional[int] = None
    course_title: Optional[str] = None
    title: str
    description: Optional[str] = None
    passing_percentage: float = 70.0
    time_limit_minutes: int = 15
    questions: List[QuestionResponse] = []
    total_questions: int = 0
    total_marks: float = 0.0

    model_config = ConfigDict(from_attributes=True)


class QuestionAnswerSubmit(BaseModel):
    question_id: int
    selected_option_id: int


class AssessmentSubmit(BaseModel):
    answers: List[QuestionAnswerSubmit]


class QuestionResultDetail(BaseModel):
    question_id: int
    question_text: str
    selected_option_id: Optional[int]
    correct_option_id: int
    is_correct: bool
    explanation: Optional[str] = None


class AssessmentResultResponse(BaseModel):
    attempt_id: int
    assessment_id: int
    score: float
    total_marks: float
    percentage: float
    passing_percentage: float
    is_passed: bool
    attempt_number: int
    next_module_unlocked: bool
    course_completed: bool = False
    certificate_id: Optional[str] = None
    feedback_message: str
    question_results: List[QuestionResultDetail] = []
    attempted_at: Optional[datetime] = None


class FinalAssessmentDetail(BaseModel):
    id: int
    course_id: int
    course_title: Optional[str] = None
    title: str
    description: Optional[str] = None
    passing_percentage: float = 70.0
    time_limit_minutes: int = 30
    questions: List[QuestionResponse] = []
    total_questions: int = 0
    total_marks: float = 0.0
