from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.swap import Review, SwapSession
from app.models.enrollment import CourseEnrollment
from app.models.certificate import Certificate
from app.schemas.user import UserProfileResponse, UserUpdate, PublicUserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users & Profiles"]
)


def enrich_user_profile(user: User, db: Session) -> dict:
    enrolled_count = db.query(CourseEnrollment).filter(CourseEnrollment.user_id == user.id).count()
    completed_count = db.query(CourseEnrollment).filter(
        CourseEnrollment.user_id == user.id,
        CourseEnrollment.status == "completed"
    ).count()
    certs_count = db.query(Certificate).filter(Certificate.user_id == user.id).count()
    swaps_count = db.query(SwapSession).filter(
        (SwapSession.user1_id == user.id) | (SwapSession.user2_id == user.id),
        SwapSession.status == "completed"
    ).count()

    reviews = db.query(Review).filter(Review.reviewee_id == user.id).all()
    review_count = len(reviews)
    avg_rating = sum(r.rating for r in reviews) / review_count if review_count > 0 else 5.0

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "college": user.college,
        "branch": user.branch,
        "year": user.year,
        "degree_id": user.degree_id,
        "branch_id": user.branch_id,
        "bio": user.bio,
        "avatar_url": user.avatar_url,
        "phone": user.phone,
        "credits": user.credits,
        "reputation_score": round(avg_rating, 1),
        "is_active": user.is_active,
        "created_at": user.created_at,
        "degree": user.degree,
        "branch_rel": user.branch_rel,
        "skills_teach": user.skills_teach,
        "skills_learn": user.skills_learn,
        "courses_enrolled_count": enrolled_count,
        "courses_completed_count": completed_count,
        "certificates_count": certs_count,
        "swaps_completed_count": swaps_count,
        "average_rating": round(avg_rating, 1),
        "review_count": review_count
    }


@router.get("/me", response_model=UserProfileResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return enrich_user_profile(current_user, db)


@router.put("/me", response_model=UserProfileResponse)
def update_my_profile(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    for key, val in update_data.model_dump(exclude_unset=True).items():
        setattr(current_user, key, val)

    db.commit()
    db.refresh(current_user)
    return enrich_user_profile(current_user, db)


@router.get("", response_model=List[PublicUserResponse])
def get_students(
    search: Optional[str] = None,
    college: Optional[str] = None,
    degree_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(User).filter(User.role == "student", User.is_active == True)
    if search:
        query = query.filter(User.name.ilike(f"%{search}%"))
    if college:
        query = query.filter(User.college.ilike(f"%{college}%"))
    if degree_id:
        query = query.filter(User.degree_id == degree_id)
    
    users = query.limit(50).all()
    results = []
    for u in users:
        swaps_count = db.query(SwapSession).filter(
            (SwapSession.user1_id == u.id) | (SwapSession.user2_id == u.id),
            SwapSession.status == "completed"
        ).count()
        reviews = db.query(Review).filter(Review.reviewee_id == u.id).all()
        review_count = len(reviews)
        avg_rating = sum(r.rating for r in reviews) / review_count if review_count > 0 else 5.0

        results.append({
            "id": u.id,
            "name": u.name,
            "college": u.college,
            "branch": u.branch,
            "year": u.year,
            "bio": u.bio,
            "avatar_url": u.avatar_url,
            "reputation_score": round(avg_rating, 1),
            "skills_teach": u.skills_teach,
            "skills_learn": u.skills_learn,
            "swaps_completed_count": swaps_count,
            "average_rating": round(avg_rating, 1),
            "review_count": review_count
        })
    return results


@router.get("/{user_id}", response_model=PublicUserResponse)
def get_student_profile(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=404, detail="Student not found")
    
    swaps_count = db.query(SwapSession).filter(
        (SwapSession.user1_id == user.id) | (SwapSession.user2_id == user.id),
        SwapSession.status == "completed"
    ).count()
    reviews = db.query(Review).filter(Review.reviewee_id == user.id).all()
    review_count = len(reviews)
    avg_rating = sum(r.rating for r in reviews) / review_count if review_count > 0 else 5.0

    return {
        "id": user.id,
        "name": user.name,
        "college": user.college,
        "branch": user.branch,
        "year": user.year,
        "bio": user.bio,
        "avatar_url": user.avatar_url,
        "reputation_score": round(avg_rating, 1),
        "skills_teach": user.skills_teach,
        "skills_learn": user.skills_learn,
        "swaps_completed_count": swaps_count,
        "average_rating": round(avg_rating, 1),
        "review_count": review_count
    }
