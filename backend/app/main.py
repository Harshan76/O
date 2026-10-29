import os
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
from app.api.course_learning_routes import router as course_learning_router

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

# CORS Configuration for Vercel, localhost, and production domains
raw_origins = settings.ALLOWED_ORIGINS.strip()
if raw_origins == "*" or not raw_origins:
    cors_origins = ["*"]
else:
    cors_origins = [o.strip() for o in raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True if cors_origins != ["*"] else False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
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
app.include_router(course_learning_router, prefix="/api")

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
        "environment": settings.ENV,
        "database": "sqlite" if not settings.SUPABASE_URL else "supabase_postgresql",
        "ai_engine": "operational" if not settings.GEMINI_API_KEY else "gemini_live",
        "tutor_ready": True,
        "version": settings.VERSION
    }

if __name__ == "__main__":
    import uvicorn
    # Render provides PORT environment variable (default fallback 8000)
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=False)
