from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.academic import Category, Degree, Branch
from app.schemas.academic import (
    CategoryResponse, CategoryCreate,
    DegreeResponse, DegreeCreate,
    BranchResponse, BranchCreate
)
from app.dependencies.auth import get_current_admin


router = APIRouter(
    prefix="/academic",
    tags=["Academic Hierarchy"]
)


@router.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


@router.get("/degrees", response_model=List[DegreeResponse])
def get_degrees(
    category_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Degree)
    if category_id:
        query = query.filter(Degree.category_id == category_id)
    return query.all()


@router.get("/branches", response_model=List[BranchResponse])
def get_branches(
    degree_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Branch)
    if degree_id:
        query = query.filter(Branch.degree_id == degree_id)
    return query.all()


@router.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    existing = db.query(Category).filter(Category.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    cat = Category(**data.model_dump())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


@router.post("/degrees", response_model=DegreeResponse, status_code=status.HTTP_201_CREATED)
def create_degree(
    data: DegreeCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    deg = Degree(**data.model_dump())
    db.add(deg)
    db.commit()
    db.refresh(deg)
    return deg


@router.post("/branches", response_model=BranchResponse, status_code=status.HTTP_201_CREATED)
def create_branch(
    data: BranchCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    br = Branch(**data.model_dump())
    db.add(br)
    db.commit()
    db.refresh(br)
    return br
