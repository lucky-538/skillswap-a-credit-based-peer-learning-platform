from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.schemas.skill import SkillResponse
from app.schemas.user import UserResponse


class SwapRequestCreate(BaseModel):
    receiver_id: int
    offered_skill_id: Optional[int] = None
    requested_skill_id: Optional[int] = None
    message: Optional[str] = None


class SwapRequestResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    offered_skill_id: Optional[int] = None
    requested_skill_id: Optional[int] = None
    message: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    sender: UserResponse
    receiver: UserResponse
    offered_skill: Optional[SkillResponse] = None
    requested_skill: Optional[SkillResponse] = None

    model_config = ConfigDict(from_attributes=True)


class SwapSessionCreate(BaseModel):
    request_id: Optional[int] = None
    user2_id: int
    title: str
    description: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    duration_minutes: int = 60
    meeting_type: str = "online"  # online, in-person
    meeting_link_or_location: Optional[str] = None


class SwapSessionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    meeting_type: Optional[str] = None
    meeting_link_or_location: Optional[str] = None
    status: Optional[str] = None  # scheduled, in-progress, completed, cancelled


class SwapSessionResponse(BaseModel):
    id: int
    request_id: Optional[int] = None
    user1_id: int
    user2_id: int
    title: str
    description: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    duration_minutes: int
    meeting_type: str
    meeting_link_or_location: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    user1: UserResponse
    user2: UserResponse

    model_config = ConfigDict(from_attributes=True)


class ReviewCreate(BaseModel):
    session_id: Optional[int] = None
    reviewee_id: int
    rating: int  # 1 to 5
    review_text: Optional[str] = None


class ReviewResponse(BaseModel):
    id: int
    session_id: Optional[int] = None
    reviewer_id: int
    reviewee_id: int
    rating: int
    review_text: Optional[str] = None
    created_at: Optional[datetime] = None
    reviewer: UserResponse

    model_config = ConfigDict(from_attributes=True)
