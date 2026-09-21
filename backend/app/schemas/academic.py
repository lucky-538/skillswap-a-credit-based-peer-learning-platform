from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class BranchBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


class BranchCreate(BranchBase):
    degree_id: int


class BranchResponse(BranchBase):
    id: int
    degree_id: int

    model_config = ConfigDict(from_attributes=True)


class DegreeBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


class DegreeCreate(DegreeBase):
    category_id: int


class DegreeResponse(DegreeBase):
    id: int
    category_id: int
    branches: List[BranchResponse] = []

    model_config = ConfigDict(from_attributes=True)


class CategoryBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    icon: Optional[str] = "BookOpen"


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int
    degrees: List[DegreeResponse] = []

    model_config = ConfigDict(from_attributes=True)
