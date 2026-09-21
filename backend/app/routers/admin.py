from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_admin
from app.models.user import User
from app.models.skill import Skill
from app.models.academic import Category, Degree, Branch
from app.models.course import Course, CourseModule, Lesson
from app.models.enrollment import CourseEnrollment
from app.models.swap import SwapSession
from app.models.certificate import Certificate
from app.models.assessment import ModuleAssessment, AssessmentQuestion, AssessmentOption
from app.schemas.admin import AdminStatsResponse, UserStatusUpdate
from app.schemas.user import UserResponse
from app.schemas.course import ModuleCreate, ModuleResponse, LessonCreate, LessonResponse
from app.schemas.assessment import ModuleAssessmentCreate, QuestionCreate
from app.schemas.certificate import CertificateResponse


router = APIRouter(
    prefix="/admin",
    tags=["Admin Control Center"]
)


@router.get("/stats", response_model=AdminStatsResponse)
def get_admin_dashboard_stats(
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    students_count = db.query(User).filter(User.role == "student").count()
    courses_count = db.query(Course).count()
    enrollments_count = db.query(CourseEnrollment).count()
    swaps_count = db.query(SwapSession).filter(SwapSession.status == "completed").count()
    completions_count = db.query(CourseEnrollment).filter(CourseEnrollment.status == "completed").count()
    certificates_count = db.query(Certificate).count()
    skills_count = db.query(Skill).count()
    categories_count = db.query(Category).count()

    return AdminStatsResponse(
        total_students=students_count,
        total_courses=courses_count,
        total_enrollments=enrollments_count,
        total_skill_swaps=swaps_count,
        completed_courses=completions_count,
        certificates_issued=certificates_count,
        total_skills=skills_count,
        total_categories=categories_count
    )


@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    role: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    if search:
        query = query.filter(User.name.ilike(f"%{search}%") | User.email.ilike(f"%{search}%"))
    return query.order_by(User.created_at.desc()).all()


@router.put("/users/{user_id}/status", response_model=UserResponse)
def update_user_status(
    user_id: int,
    data: UserStatusUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = data.is_active
    if data.role:
        user.role = data.role

    db.commit()
    db.refresh(user)
    return user


@router.post("/modules", response_model=ModuleResponse, status_code=status.HTTP_201_CREATED)
def create_course_module(
    data: ModuleCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    course = db.query(Course).filter(Course.id == data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    mod = CourseModule(**data.model_dump())
    db.add(mod)
    db.commit()
    db.refresh(mod)
    return {
        "id": mod.id,
        "course_id": mod.course_id,
        "title": mod.title,
        "description": mod.description,
        "order_index": mod.order_index,
        "has_assessment": False,
        "lessons": [],
        "created_at": mod.created_at
    }


@router.post("/lessons", response_model=LessonResponse, status_code=status.HTTP_201_CREATED)
def create_lesson(
    data: LessonCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    mod = db.query(CourseModule).filter(CourseModule.id == data.module_id).first()
    if not mod:
        raise HTTPException(status_code=404, detail="Module not found")

    lesson = Lesson(**data.model_dump())
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson


@router.post("/assessments", status_code=status.HTTP_201_CREATED)
def create_module_assessment_admin(
    data: ModuleAssessmentCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    mod = db.query(CourseModule).filter(CourseModule.id == data.module_id).first()
    if not mod:
        raise HTTPException(status_code=404, detail="Module not found")

    existing = db.query(ModuleAssessment).filter(ModuleAssessment.module_id == data.module_id).first()
    if existing:
        assessment = existing
        assessment.title = data.title
        assessment.description = data.description
        assessment.passing_percentage = data.passing_percentage
        assessment.time_limit_minutes = data.time_limit_minutes
    else:
        assessment = ModuleAssessment(
            module_id=data.module_id,
            title=data.title,
            description=data.description,
            passing_percentage=data.passing_percentage,
            time_limit_minutes=data.time_limit_minutes
        )
        db.add(assessment)
        db.flush()

    for q_data in data.questions:
        q = AssessmentQuestion(
            assessment_id=assessment.id,
            question_text=q_data.question_text,
            explanation=q_data.explanation,
            marks=q_data.marks,
            order_index=q_data.order_index
        )
        db.add(q)
        db.flush()

        for opt_data in q_data.options:
            opt = AssessmentOption(
                question_id=q.id,
                option_text=opt_data.option_text,
                is_correct=opt_data.is_correct
            )
            db.add(opt)

    db.commit()
    return {"status": "success", "assessment_id": assessment.id, "questions_count": len(data.questions)}


@router.get("/certificates", response_model=List[CertificateResponse])
def get_all_certificates(
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    return db.query(Certificate).order_by(Certificate.issue_date.desc()).all()
