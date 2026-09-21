from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database.database import Base, engine
import app.models  # load all models for metadata creation

from app.routers.auth import router as auth_router
from app.routers.academic import router as academic_router
from app.routers.users import router as users_router
from app.routers.skills import router as skills_router
from app.routers.matches import router as matches_router
from app.routers.swaps import router as swaps_router
from app.routers.courses import router as courses_router
from app.routers.enrollments import router as enrollments_router
from app.routers.assessments import router as assessments_router
from app.routers.certificates import router as certificates_router
from app.routers.notifications import router as notifications_router
from app.routers.admin import router as admin_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="SkillSwap Campus API",
    description=(
        "Production-grade E-Learning, Peer-to-Peer Skill Exchange, "
        "Assessment, and Certification platform for college students."
    ),
    version="2.0.0"
)

# CORS middleware for seamless frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (e.g. http://localhost:5173)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers with distinct tags
app.include_router(auth_router)
app.include_router(academic_router)
app.include_router(users_router)
app.include_router(skills_router)
app.include_router(matches_router)
app.include_router(swaps_router)
app.include_router(courses_router)
app.include_router(enrollments_router)
app.include_router(assessments_router)
app.include_router(certificates_router)
app.include_router(notifications_router)
app.include_router(admin_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to SkillSwap Campus API",
        "platform": "E-Learning + Peer-to-Peer Skill Exchange + Assessment + Certification",
        "version": "2.0.0",
        "status": "running"
    }


@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
            "engine": "MySQL 8 / PyMySQL"
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }