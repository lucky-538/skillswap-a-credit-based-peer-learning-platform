from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.course import Course, CourseModule, Lesson
from app.models.enrollment import CourseEnrollment, LessonProgress
from app.models.assessment import AssessmentAttempt, FinalAttempt
from app.models.certificate import Certificate
from app.models.notification import Notification
from app.schemas.enrollment import EnrollmentResponse, LearningCourseView, LearningModule, LearningLesson
from app.routers.courses import format_course_response


router = APIRouter(
    prefix="/enrollments",
    tags=["Enrollments & Learning LMS"]
)


def calculate_progress(enrollment_id: int, user_id: int, course_id: int, db: Session) -> float:
    # Total items = total lessons + total module assessments + 1 final assessment
    total_lessons = db.query(Lesson).join(CourseModule).filter(CourseModule.course_id == course_id).count()
    if total_lessons == 0:
        return 0.0

    completed_lessons = db.query(LessonProgress).filter(
        LessonProgress.enrollment_id == enrollment_id,
        LessonProgress.is_completed == True
    ).count()

    progress = min(100.0, round((completed_lessons / total_lessons) * 100, 1))
    return progress


@router.post("/courses/{course_id}/enroll", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def enroll_course(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(Course.id == course_id, Course.is_published == True).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    existing = db.query(CourseEnrollment).filter(
        CourseEnrollment.user_id == current_user.id,
        CourseEnrollment.course_id == course_id
    ).first()
    if existing:
        return {
            "id": existing.id,
            "user_id": existing.user_id,
            "course_id": existing.course_id,
            "enrolled_at": existing.enrolled_at,
            "progress_percentage": existing.progress_percentage,
            "status": existing.status,
            "completed_at": existing.completed_at,
            "course": format_course_response(course)
        }

    enrollment = CourseEnrollment(
        user_id=current_user.id,
        course_id=course_id,
        progress_percentage=0.0,
        status="in-progress"
    )
    db.add(enrollment)
    course.enrollment_count += 1

    notif = Notification(
        user_id=current_user.id,
        title="Course Enrollment Confirmed",
        message=f"You have successfully enrolled in '{course.title}'! Happy learning!",
        type="course_enroll",
        link_url=f"/learn/{course.id}"
    )
    db.add(notif)
    db.commit()
    db.refresh(enrollment)

    return {
        "id": enrollment.id,
        "user_id": enrollment.user_id,
        "course_id": enrollment.course_id,
        "enrolled_at": enrollment.enrolled_at,
        "progress_percentage": enrollment.progress_percentage,
        "status": enrollment.status,
        "completed_at": enrollment.completed_at,
        "course": format_course_response(course)
    }


@router.get("/my-courses", response_model=List[EnrollmentResponse])
def get_my_courses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    enrollments = db.query(CourseEnrollment).filter(
        CourseEnrollment.user_id == current_user.id
    ).order_by(CourseEnrollment.enrolled_at.desc()).all()

    results = []
    for e in enrollments:
        if e.course:
            results.append({
                "id": e.id,
                "user_id": e.user_id,
                "course_id": e.course_id,
                "enrolled_at": e.enrolled_at,
                "progress_percentage": e.progress_percentage,
                "status": e.status,
                "completed_at": e.completed_at,
                "course": format_course_response(e.course)
            })
    return results


@router.get("/courses/{course_id}/learn", response_model=LearningCourseView)
def get_course_learning_view(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    enrollment = db.query(CourseEnrollment).filter(
        CourseEnrollment.user_id == current_user.id,
        CourseEnrollment.course_id == course_id
    ).first()

    if not enrollment:
        # Auto-enroll for seamless viewing
        enrollment = CourseEnrollment(
            user_id=current_user.id,
            course_id=course_id,
            progress_percentage=0.0,
            status="in-progress"
        )
        db.add(enrollment)
        course.enrollment_count += 1
        db.commit()
        db.refresh(enrollment)

    # Completed lessons set
    completed_lesson_ids = {
        lp.lesson_id for lp in db.query(LessonProgress).filter(
            LessonProgress.enrollment_id == enrollment.id,
            LessonProgress.is_completed == True
        ).all()
    }

    learning_modules: List[LearningModule] = []
    is_previous_module_completed = True  # Module 1 starts unlocked

    all_modules_passed = True

    for mod in course.modules:
        mod_lessons = []
        lessons_completed_count = 0
        for les in mod.lessons:
            is_comp = les.id in completed_lesson_ids
            if is_comp:
                lessons_completed_count += 1
            mod_lessons.append(LearningLesson(
                id=les.id,
                module_id=les.module_id,
                title=les.title,
                description=les.description,
                content_text=les.content_text,
                video_url=les.video_url,
                resource_url=les.resource_url,
                duration_minutes=les.duration_minutes,
                order_index=les.order_index,
                is_completed=is_comp
            ))

        # Check module assessment
        assessment_id = mod.assessment.id if mod.assessment else None
        assessment_passed = False
        assessment_score = None
        if mod.assessment:
            passed_attempt = db.query(AssessmentAttempt).filter(
                AssessmentAttempt.assessment_id == mod.assessment.id,
                AssessmentAttempt.user_id == current_user.id,
                AssessmentAttempt.is_passed == True
            ).order_by(AssessmentAttempt.score.desc()).first()
            if passed_attempt:
                assessment_passed = True
                assessment_score = passed_attempt.percentage
            else:
                all_modules_passed = False
        else:
            assessment_passed = True

        all_lessons_done = (len(mod.lessons) > 0 and lessons_completed_count == len(mod.lessons))
        is_mod_complete = all_lessons_done and assessment_passed

        # Module unlocking rule
        is_unlocked = is_previous_module_completed

        learning_modules.append(LearningModule(
            id=mod.id,
            course_id=mod.course_id,
            title=mod.title,
            description=mod.description,
            order_index=mod.order_index,
            is_unlocked=is_unlocked,
            is_completed=is_mod_complete,
            lessons_completed_count=lessons_completed_count,
            total_lessons_count=len(mod.lessons),
            assessment_id=assessment_id,
            assessment_passed=assessment_passed,
            assessment_score=assessment_score,
            lessons=mod_lessons
        ))

        # Next module is unlocked only if this module is completed (lessons + assessment)
        is_previous_module_completed = is_unlocked and is_mod_complete

    # Final assessment check
    final_assessment_unlocked = all_modules_passed and (len(course.modules) > 0)
    final_assessment_passed = False
    if course.final_assessment:
        final_attempt = db.query(FinalAttempt).filter(
            FinalAttempt.final_assessment_id == course.final_assessment.id,
            FinalAttempt.user_id == current_user.id,
            FinalAttempt.is_passed == True
        ).first()
        if final_attempt:
            final_assessment_passed = True

    cert = db.query(Certificate).filter(
        Certificate.user_id == current_user.id,
        Certificate.course_id == course_id
    ).first()

    return LearningCourseView(
        course=format_course_response(course),
        enrollment={
            "id": enrollment.id,
            "user_id": enrollment.user_id,
            "course_id": enrollment.course_id,
            "enrolled_at": enrollment.enrolled_at,
            "progress_percentage": enrollment.progress_percentage,
            "status": enrollment.status,
            "completed_at": enrollment.completed_at,
            "course": format_course_response(course)
        },
        modules=learning_modules,
        final_assessment_unlocked=final_assessment_unlocked,
        final_assessment_passed=final_assessment_passed,
        certificate_id=cert.certificate_id if cert else None
    )


@router.post("/lessons/{lesson_id}/complete")
def complete_lesson(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    course_id = lesson.module.course_id
    enrollment = db.query(CourseEnrollment).filter(
        CourseEnrollment.user_id == current_user.id,
        CourseEnrollment.course_id == course_id
    ).first()

    if not enrollment:
        enrollment = CourseEnrollment(
            user_id=current_user.id,
            course_id=course_id,
            progress_percentage=0.0,
            status="in-progress"
        )
        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)

    progress_record = db.query(LessonProgress).filter(
        LessonProgress.enrollment_id == enrollment.id,
        LessonProgress.lesson_id == lesson_id
    ).first()

    if not progress_record:
        progress_record = LessonProgress(
            enrollment_id=enrollment.id,
            user_id=current_user.id,
            lesson_id=lesson_id,
            is_completed=True,
            completed_at=datetime.utcnow()
        )
        db.add(progress_record)
    else:
        progress_record.is_completed = True
        progress_record.completed_at = datetime.utcnow()

    db.commit()

    # Recalculate progress
    new_progress = calculate_progress(enrollment.id, current_user.id, course_id, db)
    enrollment.progress_percentage = new_progress
    db.commit()

    return {
        "status": "success",
        "lesson_id": lesson_id,
        "is_completed": True,
        "progress_percentage": new_progress
    }
