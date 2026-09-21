import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.certificate import Certificate
from app.schemas.certificate import CertificateResponse, CertificateVerifyResponse
from app.services.certificate_service import generate_certificate_pdf


router = APIRouter(
    prefix="/certificates",
    tags=["Certificates & Verification"]
)


@router.get("", response_model=List[CertificateResponse])
def get_my_certificates(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Certificate).filter(
        Certificate.user_id == current_user.id
    ).order_by(Certificate.issue_date.desc()).all()


@router.get("/{id}", response_model=CertificateResponse)
def get_certificate_detail(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cert = db.query(Certificate).filter(Certificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return cert


@router.get("/{id}/download")
def download_certificate_pdf(
    id: int,
    db: Session = Depends(get_db)
):
    cert = db.query(Certificate).filter(Certificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")

    if not cert.pdf_path or not os.path.exists(cert.pdf_path):
        # Regenerate PDF
        pdf_path = generate_certificate_pdf(
            certificate_id=cert.certificate_id,
            student_name=cert.student_name,
            course_title=cert.course_title,
            issue_date=cert.issue_date,
            grade=cert.grade,
            instructor_name=cert.course.instructor_name if cert.course else "SkillSwap Campus Faculty"
        )
        cert.pdf_path = pdf_path
        db.commit()

    return FileResponse(
        path=cert.pdf_path,
        media_type="application/pdf",
        filename=f"Certificate_{cert.certificate_id}.pdf"
    )


@router.get("/verify/{certificate_id}", response_model=CertificateVerifyResponse)
def verify_certificate_public(
    certificate_id: str,
    db: Session = Depends(get_db)
):
    cert = db.query(Certificate).filter(Certificate.certificate_id == certificate_id.strip()).first()
    if not cert:
        return CertificateVerifyResponse(
            is_valid=False,
            certificate_id=certificate_id,
            student_name=None,
            course_title=None,
            issue_date=None,
            grade=None,
            institution="SkillSwap Campus Academy",
            status="INVALID",
            verification_message="No authentic certificate record was found matching this certificate identifier in the SkillSwap Campus registry."
        )

    return CertificateVerifyResponse(
        is_valid=True,
        certificate_id=cert.certificate_id,
        student_name=cert.student_name,
        course_title=cert.course_title,
        issue_date=cert.issue_date,
        grade=cert.grade,
        institution="SkillSwap Campus Academy",
        status="VALID",
        verification_message="This certificate is officially verified and recognized as an authentic academic completion from SkillSwap Campus Academy."
    )
