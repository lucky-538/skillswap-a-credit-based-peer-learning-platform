from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from app.schemas.skill import SkillResponse
from app.schemas.user import PublicUserResponse


class PeerMatch(BaseModel):
    user: PublicUserResponse
    matching_skill: SkillResponse
    match_type: str  # "direct_swap" (both teach each other) or "tutor"
    match_score: int  # percentage score e.g. 100%, 85%
    teaches_skill: str
    wants_to_learn: Optional[str] = None
    rating: float = 5.0
    same_college: bool = False


class FallbackCourse(BaseModel):
    id: int
    title: str
    slug: str
    category_name: str
    difficulty: str
    duration_hours: int
    modules_count: int
    rating: float
    thumbnail_url: Optional[str] = None
    description: str
    certificate_available: bool = True


class SmartMatchResult(BaseModel):
    requested_skill: str
    peers_found_count: int
    matches: List[PeerMatch] = []
    fallback_recommended: bool = False
    fallback_course: Optional[FallbackCourse] = None
