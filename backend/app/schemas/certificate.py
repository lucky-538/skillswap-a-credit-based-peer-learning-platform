from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class CertificateResponse(BaseModel):
    id: int
    certificate_id: str
    user_id: int
    course_id: int
    issue_date: Optional[datetime] = None
    student_name: str
    course_title: str
    grade: str
    verification_url: str
    pdf_path: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class CertificateVerifyResponse(BaseModel):
    is_valid: bool
    certificate_id: str
    student_name: Optional[str] = None
    course_title: Optional[str] = None
    issue_date: Optional[datetime] = None
    grade: Optional[str] = None
    institution: str = "SkillSwap Campus Academy"
    status: str = "VALID"
    verification_message: str
