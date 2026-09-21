from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.swap import SkillSwapRequest, SwapSession, Review
from app.models.notification import Notification
from app.schemas.swap import (
    SwapRequestCreate, SwapRequestResponse,
    SwapSessionCreate, SwapSessionUpdate, SwapSessionResponse,
    ReviewCreate, ReviewResponse
)


router = APIRouter(
    prefix="/swaps",
    tags=["Skill Swaps & Sessions"]
)


@router.post("/requests", response_model=SwapRequestResponse, status_code=status.HTTP_201_CREATED)
def create_swap_request(
    data: SwapRequestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if data.receiver_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot send swap request to yourself")

    receiver = db.query(User).filter(User.id == data.receiver_id, User.is_active == True).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Recipient student not found")

    request = SkillSwapRequest(
        sender_id=current_user.id,
        receiver_id=data.receiver_id,
        offered_skill_id=data.offered_skill_id,
        requested_skill_id=data.requested_skill_id,
        message=data.message,
        status="pending"
    )
    db.add(request)
    db.commit()
    db.refresh(request)

    # Notify receiver
    notif = Notification(
        user_id=data.receiver_id,
        title="New Skill Swap Request",
        message=f"{current_user.name} sent you a skill swap request!",
        type="swap_request",
        link_url="/swap-requests"
    )
    db.add(notif)
    db.commit()

    return request


@router.get("/requests", response_model=List[SwapRequestResponse])
def get_swap_requests(
    type: str = "all",  # all, incoming, outgoing
    status_filter: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(SkillSwapRequest)
    if type == "incoming":
        query = query.filter(SkillSwapRequest.receiver_id == current_user.id)
    elif type == "outgoing":
        query = query.filter(SkillSwapRequest.sender_id == current_user.id)
    else:
        query = query.filter(
            or_(
                SkillSwapRequest.sender_id == current_user.id,
                SkillSwapRequest.receiver_id == current_user.id
            )
        )

    if status_filter:
        query = query.filter(SkillSwapRequest.status == status_filter)

    return query.order_by(SkillSwapRequest.created_at.desc()).all()


@router.put("/requests/{id}/accept", response_model=SwapRequestResponse)
def accept_swap_request(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    request = db.query(SkillSwapRequest).filter(SkillSwapRequest.id == id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    if request.receiver_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only recipient can accept request")

    request.status = "accepted"

    # Automatically create a Swap Session for scheduling
    session_title = f"Skill Swap: {request.offered_skill.name if request.offered_skill else 'Knowledge'} ↔ {request.requested_skill.name if request.requested_skill else 'Learning'}"
    new_session = SwapSession(
        request_id=request.id,
        user1_id=request.sender_id,
        user2_id=request.receiver_id,
        title=session_title,
        description=request.message,
        meeting_type="online",
        meeting_link_or_location="https://meet.google.com/new",
        status="scheduled"
    )
    db.add(new_session)

    # Notify sender
    notif = Notification(
        user_id=request.sender_id,
        title="Skill Swap Accepted!",
        message=f"{current_user.name} accepted your skill swap request! A learning session has been created.",
        type="swap_accepted",
        link_url="/swap-requests"
    )
    db.add(notif)
    db.commit()
    db.refresh(request)
    return request


@router.put("/requests/{id}/reject", response_model=SwapRequestResponse)
def reject_swap_request(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    request = db.query(SkillSwapRequest).filter(SkillSwapRequest.id == id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    if request.receiver_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only recipient can reject request")

    request.status = "rejected"
    
    notif = Notification(
        user_id=request.sender_id,
        title="Skill Swap Request Update",
        message=f"{current_user.name} was unable to accept your skill swap request at this time.",
        type="swap_rejected",
        link_url="/swap-requests"
    )
    db.add(notif)
    db.commit()
    db.refresh(request)
    return request


@router.put("/requests/{id}/cancel", response_model=SwapRequestResponse)
def cancel_swap_request(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    request = db.query(SkillSwapRequest).filter(SkillSwapRequest.id == id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    if request.sender_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only sender can cancel request")

    request.status = "cancelled"
    db.commit()
    db.refresh(request)
    return request


@router.get("/sessions", response_model=List[SwapSessionResponse])
def get_swap_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(SwapSession).filter(
        or_(
            SwapSession.user1_id == current_user.id,
            SwapSession.user2_id == current_user.id
        )
    ).order_by(SwapSession.created_at.desc()).all()


@router.put("/sessions/{id}/complete", response_model=SwapSessionResponse)
def complete_swap_session(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = db.query(SwapSession).filter(SwapSession.id == id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.user1_id != current_user.id and session.user2_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized for this session")

    session.status = "completed"
    if session.request:
        session.request.status = "completed"

    # Reward credits
    other_user_id = session.user2_id if session.user1_id == current_user.id else session.user1_id
    other_user = db.query(User).filter(User.id == other_user_id).first()
    if other_user:
        other_user.credits += 5
    current_user.credits += 5

    db.commit()
    db.refresh(session)
    return session


@router.post("/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(
    data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if data.reviewee_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot review yourself")

    if data.rating < 1 or data.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

    # Prevent duplicate review on same session
    if data.session_id:
        existing = db.query(Review).filter(
            Review.session_id == data.session_id,
            Review.reviewer_id == current_user.id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="You have already reviewed this session")

    review = Review(
        session_id=data.session_id,
        reviewer_id=current_user.id,
        reviewee_id=data.reviewee_id,
        rating=data.rating,
        review_text=data.review_text
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review
