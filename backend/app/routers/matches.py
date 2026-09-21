from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.skill import Skill
from app.models.user_skill import UserSkillTeach, UserSkillLearn
from app.models.course import Course
from app.models.swap import Review, SwapSession
from app.schemas.match import SmartMatchResult, PeerMatch, FallbackCourse
from app.schemas.skill import SkillResponse


router = APIRouter(
    prefix="/matches",
    tags=["Skill Matching & Recommendations"]
)


@router.get("", response_model=SmartMatchResult)
def find_skill_matches(
    skill_id: Optional[int] = Query(None, description="Specific skill ID to search tutors for"),
    skill_name: Optional[str] = Query(None, description="Skill name to search"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    target_skill = None
    if skill_id:
        target_skill = db.query(Skill).filter(Skill.id == skill_id).first()
    elif skill_name:
        target_skill = db.query(Skill).filter(Skill.name.ilike(skill_name.strip())).first()
    else:
        # Default to first skill current user wants to learn
        first_learn = db.query(UserSkillLearn).filter(UserSkillLearn.user_id == current_user.id).first()
        if first_learn:
            target_skill = first_learn.skill

    if not target_skill and not skill_name:
        return SmartMatchResult(
            requested_skill="None selected",
            peers_found_count=0,
            matches=[],
            fallback_recommended=False,
            fallback_course=None
        )

    requested_skill_name = target_skill.name if target_skill else (skill_name or "General Skill")

    # Get skills the current user can teach
    my_taught_skill_ids = [s.skill_id for s in db.query(UserSkillTeach).filter(UserSkillTeach.user_id == current_user.id).all()]

    peer_matches: List[PeerMatch] = []

    if target_skill:
        # Find other users teaching this skill
        teachers = db.query(UserSkillTeach).filter(
            UserSkillTeach.skill_id == target_skill.id,
            UserSkillTeach.user_id != current_user.id
        ).all()

        for t in teachers:
            user = t.user
            if not user or not user.is_active:
                continue

            # Check if this teacher wants any skill the current user can teach
            their_learn_skill_ids = [l.skill_id for l in user.skills_learn]
            mutual_skill_ids = set(my_taught_skill_ids).intersection(set(their_learn_skill_ids))

            is_direct_swap = len(mutual_skill_ids) > 0
            
            # Calculate Match Score
            base_score = 70
            if is_direct_swap:
                base_score = 100
                match_type = "direct_swap"
            else:
                match_type = "tutor"
                if user.college and current_user.college and user.college.lower() == current_user.college.lower():
                    base_score += 15
                if user.degree_id and current_user.degree_id and user.degree_id == current_user.degree_id:
                    base_score += 10

            reviews = db.query(Review).filter(Review.reviewee_id == user.id).all()
            review_count = len(reviews)
            avg_rating = sum(r.rating for r in reviews) / review_count if review_count > 0 else 5.0

            swaps_count = db.query(SwapSession).filter(
                (SwapSession.user1_id == user.id) | (SwapSession.user2_id == user.id),
                SwapSession.status == "completed"
            ).count()

            wants_str = ", ".join([l.skill.name for l in user.skills_learn[:3]]) if user.skills_learn else "General Skills"

            peer_matches.append(PeerMatch(
                user={
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
                },
                matching_skill=SkillResponse.model_validate(target_skill),
                match_type=match_type,
                match_score=min(100, base_score),
                teaches_skill=target_skill.name,
                wants_to_learn=wants_str,
                rating=round(avg_rating, 1),
                same_college=(bool(user.college and current_user.college and user.college.lower() == current_user.college.lower()))
            ))

    # Sort matches: direct_swap first, then by match_score descending, then rating
    peer_matches.sort(key=lambda m: (m.match_type == "direct_swap", m.match_score, m.rating), reverse=True)

    fallback_course = None
    fallback_recommended = False

    # If no peer is available, recommend a matching course from the catalog
    if len(peer_matches) == 0:
        fallback_recommended = True
        
        # Search for a course mapped to this skill or with title/description matching the skill name
        course = None
        if target_skill:
            course = db.query(Course).filter(
                (Course.skill_id == target_skill.id) |
                (Course.title.ilike(f"%{target_skill.name}%"))
            ).first()

        if not course:
            course = db.query(Course).filter(
                or_(
                    Course.title.ilike(f"%{requested_skill_name}%"),
                    Course.description.ilike(f"%{requested_skill_name}%")
                )
            ).first()

        if not course:
            # Pick any popular featured course as default fallback
            course = db.query(Course).order_by(Course.rating.desc(), Course.enrollment_count.desc()).first()

        if course:
            fallback_course = FallbackCourse(
                id=course.id,
                title=course.title,
                slug=course.slug,
                category_name=course.category.name if course.category else "General",
                difficulty=course.difficulty,
                duration_hours=course.duration_hours,
                modules_count=len(course.modules),
                rating=course.rating,
                thumbnail_url=course.thumbnail_url,
                description=course.description,
                certificate_available=True
            )

    return SmartMatchResult(
        requested_skill=requested_skill_name,
        peers_found_count=len(peer_matches),
        matches=peer_matches,
        fallback_recommended=fallback_recommended,
        fallback_course=fallback_course
    )
