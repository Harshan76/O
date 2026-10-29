from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.db.storage import init_db, seed_initial_catalog
from app.db.scenarios import load_scenario
from app.api.profile_routes import router as profile_router
from app.api.course_goal_routes import router as course_goal_router
from app.api.assessment_routes import router as assessment_router
from app.api.roadmap_routes import router as roadmap_router
from app.api.tutor_routes import router as tutor_router
from app.api.study_routes import router as study_router
from app.api.challenge_routes import router as challenge_router
from app.api.project_routes import router as project_router
from app.api.progress_routes import router as progress_router
from app.api.demo_routes import router as demo_router

# Initialize Database and Seed Catalogs
init_db()
seed_initial_catalog()

# Pre-seed Scenario 1 for instant demo readiness
try:
    load_scenario("1")
except Exception as e:
    print(f"Scenario 1 pre-seed note: {e}")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="SkillForge AI — Personal AI Tutor & Adaptive Learning Platform (Learner-Only Architecture)"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(profile_router, prefix="/api")
app.include_router(course_goal_router, prefix="/api")
app.include_router(assessment_router, prefix="/api")
app.include_router(roadmap_router, prefix="/api")
app.include_router(tutor_router, prefix="/api")
app.include_router(study_router, prefix="/api")
app.include_router(challenge_router, prefix="/api")
app.include_router(project_router, prefix="/api")
app.include_router(progress_router, prefix="/api")
app.include_router(demo_router, prefix="/api")

@app.get("/")
def root():
    return {
        "platform": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "mode": "Learner-Only AI Tutor & Adaptive Platform",
        "docs_url": "/docs",
        "status": "operational"
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "database": "sqlite_persistent",
        "ai_engine": "operational",
        "tutor_ready": True
    }
