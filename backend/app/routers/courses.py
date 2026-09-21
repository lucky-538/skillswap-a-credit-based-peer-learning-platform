from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database.database import get_db
from app.dependencies.auth import get_current_admin, get_current_user
from app.models.course import Course, CourseModule, Lesson
from app.models.user import User
from app.models.user_skill import UserSkillLearn
from app.models.enrollment import CourseEnrollment
from app.schemas.course import (
    CourseResponse, CourseDetailResponse, CourseCreate, CourseUpdate
)


router = APIRouter(
    prefix="/courses",
    tags=["Courses & Catalog"]
)


def format_course_response(course: Course) -> dict:
    return {
        "id": course.id,
        "title": course.title,
        "slug": course.slug,
        "category_id": course.category_id,
        "degree_id": course.degree_id,
        "branch_id": course.branch_id,
        "skill_id": course.skill_id,
        "description": course.description,
        "what_you_will_learn": course.what_you_will_learn,
        "requirements": course.requirements,
        "instructor_name": course.instructor_name,
        "difficulty": course.difficulty,
        "duration_hours": course.duration_hours,
        "thumbnail_url": course.thumbnail_url,
        "is_published": course.is_published,
        "rating": course.rating,
        "enrollment_count": course.enrollment_count,
        "modules_count": len(course.modules) if course.modules else 0,
        "category": course.category,
        "degree": course.degree,
        "branch": course.branch,
        "skill": course.skill,
        "created_at": course.created_at
    }


@router.get("", response_model=List[CourseResponse])
def get_courses(
    search: Optional[str] = Query(None, description="Search course title or description"),
    category_id: Optional[int] = None,
    degree_id: Optional[int] = None,
    branch_id: Optional[int] = None,
    skill_id: Optional[int] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Course).filter(Course.is_published == True)

    if category_id:
        query = query.filter(Course.category_id == category_id)
    if degree_id:
        query = query.filter(Course.degree_id == degree_id)
    if branch_id:
        query = query.filter(Course.branch_id == branch_id)
    if skill_id:
        query = query.filter(Course.skill_id == skill_id)
    if difficulty:
        query = query.filter(Course.difficulty.ilike(difficulty))
    if search:
        query = query.filter(
            or_(
                Course.title.ilike(f"%{search}%"),
                Course.description.ilike(f"%{search}%"),
                Course.what_you_will_learn.ilike(f"%{search}%")
            )
        )

    courses = query.order_by(Course.rating.desc(), Course.enrollment_count.desc()).all()
    return [format_course_response(c) for c in courses]


@router.get("/recommended", response_model=List[CourseResponse])
def get_recommended_courses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns personalized course recommendations based on the student's:
    1. Wishlist skills (skills_learn)
    2. Enrolled degree & branch
    3. Top trending courses not yet enrolled
    """
    # Find courses user is already enrolled in
    enrolled_course_ids = [
        e.course_id for e in db.query(CourseEnrollment).filter(CourseEnrollment.user_id == current_user.id).all()
    ]

    # Find skill IDs user wants to learn
    wanted_skill_ids = [
        sl.skill_id for sl in db.query(UserSkillLearn).filter(UserSkillLearn.user_id == current_user.id).all()
    ]

    recommended = []
    seen_course_ids = set(enrolled_course_ids)

    # 1. Match courses with wanted skills
    if wanted_skill_ids:
        skill_courses = db.query(Course).filter(
            Course.is_published == True,
            Course.skill_id.in_(wanted_skill_ids),
            Course.id.notin_(seen_course_ids)
        ).all()
        for c in skill_courses:
            if c.id not in seen_course_ids:
                recommended.append(c)
                seen_course_ids.add(c.id)

    # 2. Match courses for user's degree / branch
    if current_user.degree_id or current_user.branch_id:
        degree_query = db.query(Course).filter(
            Course.is_published == True,
            Course.id.notin_(seen_course_ids)
        )
        if current_user.branch_id:
            degree_query = degree_query.filter(Course.branch_id == current_user.branch_id)
        elif current_user.degree_id:
            degree_query = degree_query.filter(Course.degree_id == current_user.degree_id)

        for c in degree_query.limit(4).all():
            if c.id not in seen_course_ids:
                recommended.append(c)
                seen_course_ids.add(c.id)

    # 3. Fill remaining with top-rated courses
    if len(recommended) < 6:
        fallback_top = db.query(Course).filter(
            Course.is_published == True,
            Course.id.notin_(seen_course_ids)
        ).order_by(Course.rating.desc(), Course.enrollment_count.desc()).limit(6 - len(recommended)).all()

        for c in fallback_top:
            if c.id not in seen_course_ids:
                recommended.append(c)
                seen_course_ids.add(c.id)

    return [format_course_response(c) for c in recommended]


@router.get("/{id}", response_model=CourseDetailResponse)
def get_course_detail(
    id: int,
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(Course.id == id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    course_data = format_course_response(course)
    course_data["modules"] = [
        {
            "id": m.id,
            "course_id": m.course_id,
            "title": m.title,
            "description": m.description,
            "order_index": m.order_index,
            "has_assessment": m.assessment is not None,
            "lessons": m.lessons,
            "created_at": m.created_at
        }
        for m in course.modules
    ]
    course_data["has_final_assessment"] = course.final_assessment is not None
    course_data["certificate_available"] = True
    return course_data


@router.post("", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(
    data: CourseCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    slug_base = data.title.lower().replace(" ", "-").replace("/", "-")
    slug = slug_base
    count = 1
    while db.query(Course).filter(Course.slug == slug).first():
        slug = f"{slug_base}-{count}"
        count += 1

    course = Course(
        slug=slug,
        **data.model_dump()
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return format_course_response(course)


@router.put("/{id}", response_model=CourseResponse)
def update_course(
    id: int,
    data: CourseUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    course = db.query(Course).filter(Course.id == id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(course, key, val)

    db.commit()
    db.refresh(course)
    return format_course_response(course)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    course = db.query(Course).filter(Course.id == id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    db.delete(course)
    db.commit()
