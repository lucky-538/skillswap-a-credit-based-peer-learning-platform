import random
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.course import Course, CourseModule, Lesson
from app.models.enrollment import CourseEnrollment
from app.models.assessment import (
    ModuleAssessment, AssessmentQuestion, AssessmentOption,
    AssessmentAttempt, AssessmentAnswer,
    FinalAssessment, FinalAttempt
)
from app.models.certificate import Certificate
from app.models.notification import Notification
from app.schemas.assessment import (
    ModuleAssessmentDetail, AssessmentSubmit, AssessmentResultResponse,
    QuestionResultDetail, FinalAssessmentDetail
)
from app.services.certificate_service import generate_certificate_pdf


router = APIRouter(
    prefix="/assessments",
    tags=["Assessments & Mock Tests"]
)


def generate_unique_certificate_id(course_slug: str, user_id: int) -> str:
    prefix = "".join([w[0].upper() for w in course_slug.split("-")[:2]]) or "CC"
    year = datetime.now().year
    rand_num = random.randint(100000, 999999)
    return f"SSC-{prefix}-{year}-{rand_num}"


@router.get("/module/{module_id}", response_model=ModuleAssessmentDetail)
def get_module_assessment(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    module = db.query(CourseModule).filter(CourseModule.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    assessment = db.query(ModuleAssessment).filter(ModuleAssessment.module_id == module_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="No assessment found for this module")

    questions_data = []
    total_marks = 0
    for q in assessment.questions:
        total_marks += q.marks
        options_data = [{"id": o.id, "question_id": o.question_id, "option_text": o.option_text} for o in q.options]
        questions_data.append({
            "id": q.id,
            "assessment_id": q.assessment_id,
            "question_text": q.question_text,
            "marks": q.marks,
            "order_index": q.order_index,
            "options": options_data
        })

    return {
        "id": assessment.id,
        "module_id": assessment.module_id,
        "module_title": module.title,
        "course_id": module.course_id,
        "course_title": module.course.title if module.course else "",
        "title": assessment.title,
        "description": assessment.description,
        "passing_percentage": assessment.passing_percentage,
        "time_limit_minutes": assessment.time_limit_minutes,
        "questions": questions_data,
        "total_questions": len(questions_data),
        "total_marks": total_marks
    }


@router.post("/module/{assessment_id}/submit", response_model=AssessmentResultResponse)
def submit_module_assessment(
    assessment_id: int,
    data: AssessmentSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    assessment = db.query(ModuleAssessment).filter(ModuleAssessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    attempt_count = db.query(AssessmentAttempt).filter(
        AssessmentAttempt.assessment_id == assessment_id,
        AssessmentAttempt.user_id == current_user.id
    ).count()

    total_marks = sum(q.marks for q in assessment.questions)
    if total_marks == 0:
        total_marks = 1.0

    score = 0.0
    question_results: List[QuestionResultDetail] = []
    answers_to_record = []

    submitted_answers_map = {ans.question_id: ans.selected_option_id for ans in data.answers}

    for q in assessment.questions:
        correct_option = next((opt for opt in q.options if opt.is_correct), None)
        correct_opt_id = correct_option.id if correct_option else 0
        selected_opt_id = submitted_answers_map.get(q.id)

        is_correct = (selected_opt_id == correct_opt_id and selected_opt_id is not None)
        if is_correct:
            score += q.marks

        question_results.append(QuestionResultDetail(
            question_id=q.id,
            question_text=q.question_text,
            selected_option_id=selected_opt_id,
            correct_option_id=correct_opt_id,
            is_correct=is_correct,
            explanation=q.explanation
        ))

        answers_to_record.append({
            "question_id": q.id,
            "selected_option_id": selected_opt_id,
            "is_correct": is_correct
        })

    percentage = round((score / total_marks) * 100, 1)
    is_passed = percentage >= assessment.passing_percentage

    attempt = AssessmentAttempt(
        assessment_id=assessment_id,
        user_id=current_user.id,
        score=score,
        total_marks=total_marks,
        percentage=percentage,
        is_passed=is_passed,
        attempt_number=attempt_count + 1
    )
    db.add(attempt)
    db.flush()

    for ans in answers_to_record:
        db_ans = AssessmentAnswer(
            attempt_id=attempt.id,
            question_id=ans["question_id"],
            selected_option_id=ans["selected_option_id"],
            is_correct=ans["is_correct"]
        )
        db.add(db_ans)

    feedback_msg = (
        f"Congratulations! You passed the module assessment with {percentage}%! The next module is now unlocked."
        if is_passed
        else f"You scored {percentage}%. Passing score is {assessment.passing_percentage}%. Review the lessons and retake the test!"
    )

    notif = Notification(
        user_id=current_user.id,
        title=f"Module Assessment {'Passed ✓' if is_passed else 'Attempt Result'}",
        message=feedback_msg,
        type="assessment_pass" if is_passed else "assessment_fail",
        link_url=f"/learn/{assessment.module.course_id}"
    )
    db.add(notif)
    db.commit()
    db.refresh(attempt)

    return AssessmentResultResponse(
        attempt_id=attempt.id,
        assessment_id=assessment_id,
        score=score,
        total_marks=total_marks,
        percentage=percentage,
        passing_percentage=assessment.passing_percentage,
        is_passed=is_passed,
        attempt_number=attempt.attempt_number,
        next_module_unlocked=is_passed,
        course_completed=False,
        certificate_id=None,
        feedback_message=feedback_msg,
        question_results=question_results,
        attempted_at=attempt.attempted_at
    )


@router.get("/final/{course_id}", response_model=FinalAssessmentDetail)
def get_final_assessment(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    all_questions = []
    total_marks = 0
    order_idx = 1
    for mod in course.modules:
        if mod.assessment:
            for q in mod.assessment.questions:
                total_marks += q.marks
                options_data = [{"id": o.id, "question_id": o.question_id, "option_text": o.option_text} for o in q.options]
                all_questions.append({
                    "id": q.id,
                    "assessment_id": q.assessment_id,
                    "question_text": q.question_text,
                    "marks": q.marks,
                    "order_index": order_idx,
                    "options": options_data
                })
                order_idx += 1

    return {
        "id": course_id,
        "course_id": course.id,
        "course_title": course.title,
        "title": f"Final Comprehensive Examination: {course.title}",
        "description": "Complete all questions with at least 70% to graduate and receive your verified Certificate of Completion.",
        "passing_percentage": 70.0,
        "time_limit_minutes": 30,
        "questions": all_questions,
        "total_questions": len(all_questions),
        "total_marks": total_marks
    }


@router.post("/final/{course_id}/submit", response_model=AssessmentResultResponse)
def submit_final_assessment(
    course_id: int,
    data: AssessmentSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    course_questions = []
    for mod in course.modules:
        if mod.assessment:
            course_questions.extend(mod.assessment.questions)

    total_marks = sum(q.marks for q in course_questions)
    if total_marks == 0:
        total_marks = 1.0

    score = 0.0
    question_results: List[QuestionResultDetail] = []
    submitted_answers_map = {ans.question_id: ans.selected_option_id for ans in data.answers}

    for q in course_questions:
        correct_option = next((opt for opt in q.options if opt.is_correct), None)
        correct_opt_id = correct_option.id if correct_option else 0
        selected_opt_id = submitted_answers_map.get(q.id)

        is_correct = (selected_opt_id == correct_opt_id and selected_opt_id is not None)
        if is_correct:
            score += q.marks

        question_results.append(QuestionResultDetail(
            question_id=q.id,
            question_text=q.question_text,
            selected_option_id=selected_opt_id,
            correct_option_id=correct_opt_id,
            is_correct=is_correct,
            explanation=q.explanation
        ))

    percentage = round((score / total_marks) * 100, 1)
    is_passed = percentage >= 70.0

    cert_id = None
    if is_passed:
        enrollment = db.query(CourseEnrollment).filter(
            CourseEnrollment.user_id == current_user.id,
            CourseEnrollment.course_id == course_id
        ).first()

        if enrollment:
            enrollment.status = "completed"
            enrollment.progress_percentage = 100.0
            enrollment.completed_at = datetime.utcnow()

        existing_cert = db.query(Certificate).filter(
            Certificate.user_id == current_user.id,
            Certificate.course_id == course_id
        ).first()

        if not existing_cert:
            cert_id = generate_unique_certificate_id(course.slug, current_user.id)
            verification_url = f"http://localhost:5173/verify-certificate/{cert_id}"
            
            pdf_path = generate_certificate_pdf(
                certificate_id=cert_id,
                student_name=current_user.name,
                course_title=course.title,
                issue_date=datetime.utcnow(),
                grade="Distinction" if percentage >= 85 else "First Class",
                instructor_name=course.instructor_name or "SkillSwap Campus Faculty"
            )

            cert = Certificate(
                certificate_id=cert_id,
                user_id=current_user.id,
                course_id=course_id,
                student_name=current_user.name,
                course_title=course.title,
                grade="Distinction" if percentage >= 85 else "First Class",
                verification_url=verification_url,
                pdf_path=pdf_path
            )
            db.add(cert)

            notif = Notification(
                user_id=current_user.id,
                title="🎓 Certificate Issued!",
                message=f"Congratulations! You have completed '{course.title}' and earned Certificate #{cert_id}!",
                type="certificate_generated",
                link_url=f"/certificates"
            )
            db.add(notif)
        else:
            cert_id = existing_cert.certificate_id

    db.commit()

    feedback_msg = (
        f"Outstanding! You passed the Final Exam with {percentage}%! Your certificate #{cert_id} has been generated!"
        if is_passed
        else f"You scored {percentage}%. Passing score is 70.0%. Please review course materials and retake the final exam."
    )

    return AssessmentResultResponse(
        attempt_id=1,
        assessment_id=course_id,
        score=score,
        total_marks=total_marks,
        percentage=percentage,
        passing_percentage=70.0,
        is_passed=is_passed,
        attempt_number=1,
        next_module_unlocked=is_passed,
        course_completed=is_passed,
        certificate_id=cert_id,
        feedback_message=feedback_msg,
        question_results=question_results,
        attempted_at=datetime.utcnow()
    )
