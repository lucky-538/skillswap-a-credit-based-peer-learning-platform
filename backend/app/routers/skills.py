from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.skill import Skill
from app.models.user_skill import UserSkillTeach, UserSkillLearn
from app.models.user import User
from app.schemas.skill import (
    SkillResponse, SkillCreate,
    SkillTeachResponse, SkillTeachCreate,
    SkillLearnResponse, SkillLearnCreate
)


router = APIRouter(
    prefix="/skills",
    tags=["Skills & Capabilities"]
)


@router.get("", response_model=List[SkillResponse])
def get_skills(
    category_name: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Skill)
    if category_name:
        query = query.filter(Skill.category_name == category_name)
    if search:
        query = query.filter(Skill.name.ilike(f"%{search}%"))
    return query.order_by(Skill.name.asc()).all()


@router.post("", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
def create_skill(
    skill_data: SkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = db.query(Skill).filter(Skill.name.ilike(skill_data.name.strip())).first()
    if existing:
        return existing
    
    new_skill = Skill(
        name=skill_data.name.strip(),
        category_id=skill_data.category_id,
        category_name=skill_data.category_name or "General",
        description=skill_data.description
    )
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)
    return new_skill


@router.get("/user/teach", response_model=List[SkillTeachResponse])
def get_my_teaching_skills(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(UserSkillTeach).filter(UserSkillTeach.user_id == current_user.id).all()


@router.post("/user/teach", response_model=SkillTeachResponse, status_code=status.HTTP_201_CREATED)
def add_teaching_skill(
    data: SkillTeachCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    skill_id = data.skill_id
    if not skill_id and data.skill_name:
        existing_skill = db.query(Skill).filter(Skill.name.ilike(data.skill_name.strip())).first()
        if existing_skill:
            skill_id = existing_skill.id
        else:
            new_skill = Skill(
                name=data.skill_name.strip(),
                category_name=data.category_name or "Technology"
            )
            db.add(new_skill)
            db.commit()
            db.refresh(new_skill)
            skill_id = new_skill.id

    if not skill_id:
        raise HTTPException(status_code=400, detail="Skill ID or valid skill name required")

    existing_entry = db.query(UserSkillTeach).filter(
        UserSkillTeach.user_id == current_user.id,
        UserSkillTeach.skill_id == skill_id
    ).first()
    if existing_entry:
        existing_entry.proficiency_level = data.proficiency_level
        existing_entry.experience_description = data.experience_description
        db.commit()
        db.refresh(existing_entry)
        return existing_entry

    user_skill = UserSkillTeach(
        user_id=current_user.id,
        skill_id=skill_id,
        proficiency_level=data.proficiency_level,
        experience_description=data.experience_description
    )
    db.add(user_skill)
    db.commit()
    db.refresh(user_skill)
    return user_skill


@router.delete("/user/teach/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_teaching_skill(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    entry = db.query(UserSkillTeach).filter(
        UserSkillTeach.id == id,
        UserSkillTeach.user_id == current_user.id
    ).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Skill entry not found")
    db.delete(entry)
    db.commit()


@router.get("/user/learn", response_model=List[SkillLearnResponse])
def get_my_learning_skills(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(UserSkillLearn).filter(UserSkillLearn.user_id == current_user.id).all()


@router.post("/user/learn", response_model=SkillLearnResponse, status_code=status.HTTP_201_CREATED)
def add_learning_skill(
    data: SkillLearnCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    skill_id = data.skill_id
    if not skill_id and data.skill_name:
        existing_skill = db.query(Skill).filter(Skill.name.ilike(data.skill_name.strip())).first()
        if existing_skill:
            skill_id = existing_skill.id
        else:
            new_skill = Skill(
                name=data.skill_name.strip(),
                category_name=data.category_name or "Technology"
            )
            db.add(new_skill)
            db.commit()
            db.refresh(new_skill)
            skill_id = new_skill.id

    if not skill_id:
        raise HTTPException(status_code=400, detail="Skill ID or valid skill name required")

    existing_entry = db.query(UserSkillLearn).filter(
        UserSkillLearn.user_id == current_user.id,
        UserSkillLearn.skill_id == skill_id
    ).first()
    if existing_entry:
        existing_entry.desired_level = data.desired_level
        existing_entry.notes = data.notes
        db.commit()
        db.refresh(existing_entry)
        return existing_entry

    user_skill = UserSkillLearn(
        user_id=current_user.id,
        skill_id=skill_id,
        desired_level=data.desired_level,
        notes=data.notes
    )
    db.add(user_skill)
    db.commit()
    db.refresh(user_skill)
    return user_skill


@router.delete("/user/learn/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_learning_skill(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    entry = db.query(UserSkillLearn).filter(
        UserSkillLearn.id == id,
        UserSkillLearn.user_id == current_user.id
    ).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Skill entry not found")
    db.delete(entry)
    db.commit()
