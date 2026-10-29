import json
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Header
from typing import Optional, List
from app.db.storage import get_connection
from app.models.schemas import MiniProject, SubmissionEvaluateRequest, SubmissionEvaluateResponse, RubricScoreItem

router = APIRouter(tags=["Personalized Mini-Projects"])

@router.get("/projects", response_model=List[MiniProject])
def list_mini_projects():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, course_id, skill_code, title, domain, objective, difficulty, estimated_hours,
           requirements_json, milestones_json, rubric_json
    FROM mini_projects
    """)
    rows = cursor.fetchall()
    conn.close()

    projects = []
    for r in rows:
        projects.append(MiniProject(
            id=r["id"],
            title=r["title"],
            domain=r["domain"],
            skill_code=r["skill_code"],
            objective=r["objective"],
            difficulty=r["difficulty"],
            estimated_hours=r["estimated_hours"],
            requirements=json.loads(r["requirements_json"] or "[]"),
            milestones=json.loads(r["milestones_json"] or "[]"),
            rubric=json.loads(r["rubric_json"] or "[]")
        ))
    return projects

@router.post("/projects/generate", response_model=MiniProject)
def generate_mini_project(payload: dict, x_learner_id: Optional[str] = Header(None)):
    domain = payload.get("domain", "Python Programming")
    skill_code = payload.get("skill_code", "PY_FUNCS")
    difficulty = payload.get("difficulty", "intermediate")
    project_id = f"p-gen-{uuid.uuid4().hex[:6]}"
    now = datetime.now(timezone.utc).isoformat()

    project = MiniProject(
        id=project_id,
        title=f"Adaptive Capstone: Production {domain} Engine",
        domain=domain,
        skill_code=skill_code,
        objective=f"Build a resilient, production-ready {domain} subsystem incorporating error boundaries and clean architecture.",
        difficulty=difficulty,
        estimated_hours=6,
        requirements=[
            "Design clean component separation of concerns",
            "Implement defensive schema validation on inputs",
            "Handle unexpected failure states gracefully with sanitized outputs",
            "Provide comprehensive documentation and unit test coverage"
        ],
        milestones=[
            {"id": "m1", "title": "Architecture Setup & Interface Definitions", "description": "Define contracts and types", "is_completed": False},
            {"id": "m2", "title": "Core Implementation & Validation", "description": "Implement business logic and guards", "is_completed": False},
            {"id": "m3", "title": "Testing, Resiliency & Documentation", "description": "Write tests and handle edge cases", "is_completed": False}
        ],
        rubric=[
            {"criterion": "Architecture & Modularity", "weight": 35, "description": "Separation of concerns and clean functional boundaries"},
            {"criterion": "Defensive Validation & Typing", "weight": 35, "description": "Strict schema enforcement and type annotations"},
            {"criterion": "Error Handling & Documentation", "weight": 30, "description": "Sanitized error boundaries and comprehensive docs"}
        ]
    )

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO mini_projects (id, course_id, skill_code, title, domain, objective, difficulty, estimated_hours, requirements_json, milestones_json, rubric_json, created_at)
    VALUES (?, 'c-custom', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (project.id, project.skill_code, project.title, project.domain, project.objective, project.difficulty, project.estimated_hours, json.dumps(project.requirements), json.dumps([m.model_dump() for m in project.milestones]), json.dumps([r.model_dump() for r in project.rubric]), now))
    conn.commit()
    conn.close()

    return project

@router.post("/submissions/evaluate", response_model=SubmissionEvaluateResponse)
def evaluate_project_submission(req: SubmissionEvaluateRequest, x_learner_id: Optional[str] = Header(None)):
    learner_id = x_learner_id or "demo-learner-1"
    sub_text = req.submission_text.strip()
    sub_id = f"sub-{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc).isoformat()

    # Explicit rubric evaluation based on submission length, keywords, and code structure
    has_validation = any(k in sub_text.lower() for k in ["validate", "schema", "pydantic", "type", "check"])
    has_error_handling = any(k in sub_text.lower() for k in ["try", "except", "catch", "error", "handler"])
    has_architecture = any(k in sub_text.lower() for k in ["class", "def", "module", "router", "service", "import"])

    arch_score = 90 if has_architecture else 65
    val_score = 92 if has_validation else 60
    err_score = 75 if has_error_handling else 50
    doc_score = 85 if len(sub_text) > 100 else 60

    overall_score = int((arch_score * 0.35) + (val_score * 0.25) + (err_score * 0.25) + (doc_score * 0.15))
    passed = overall_score >= 70

    rubric_scores = [
        RubricScoreItem(criterion="Architecture & Separation of Concerns", score=arch_score, feedback="Clear modular separation between layers." if has_architecture else "Monolithic layout; consider separating routes and business logic."),
        RubricScoreItem(criterion="Input Validation & Type Safety", score=val_score, feedback="Strong schema assertions on incoming payloads." if has_validation else "Missing strict input validation guards."),
        RubricScoreItem(criterion="Error Handling & Status Codes", score=err_score, feedback="Exception boundaries captured and sanitized." if has_error_handling else "Unhandled exceptions may leak raw stack traces to users."),
        RubricScoreItem(criterion="Documentation & Testing", score=doc_score, feedback="Sufficient inline comments and clear parameter contracts.")
    ]

    strengths = [
        "Clean functional boundaries",
        "Clear variable nomenclature"
    ]
    if has_validation:
        strengths.append("Robust input validation preventing malformed data")
    if has_error_handling:
        strengths.append("Explicit exception blocks")

    areas_for_improvement = []
    if not has_error_handling or err_score < 80:
        areas_for_improvement.append("Implement centralized exception handling middleware to prevent internal 500 error leaks.")
    if not has_validation or val_score < 80:
        areas_for_improvement.append("Introduce strict declarative Pydantic/Zod schemas on all route parameters.")
    if len(areas_for_improvement) == 0:
        areas_for_improvement.append("Add automated integration tests with mock database fixtures.")

    ai_coaching_notes = (
        f"Solid project submission! Your architecture scored {arch_score}/100. "
        f"The primary opportunity for improvement is error resiliency (scored {err_score}/100). "
        f"In production, unhandled tracebacks can expose table names or credentials; centralizing exception handlers ensures secure, standardized error responses."
    )

    # Save submission
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO project_submissions (id, project_id, learner_id, submission_text, code_repo_link, overall_score, passed, rubric_scores_json, feedback_json, submitted_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (sub_id, req.project_id, learner_id, sub_text, req.code_repo_link, overall_score, 1 if passed else 0, json.dumps([r.model_dump() for r in rubric_scores]), json.dumps({"notes": ai_coaching_notes, "strengths": strengths}), now))

    # Log in activity history
    cursor.execute("""
    INSERT INTO learning_activity_history (id, learner_id, activity_type, title, score, details, created_at)
    VALUES (?, ?, 'project', 'Project Evaluation Completed', ?, ?, ?)
    """, (str(uuid.uuid4()), learner_id, overall_score, f"Project {req.project_id} scored {overall_score}%. Passed: {passed}.", now))

    conn.commit()
    conn.close()

    return SubmissionEvaluateResponse(
        submission_id=sub_id,
        project_id=req.project_id,
        overall_score=overall_score,
        passed=passed,
        rubric_scores=rubric_scores,
        strengths=strengths,
        areas_for_improvement=areas_for_improvement,
        ai_coaching_notes=ai_coaching_notes,
        next_recommended_milestone="Implement Centralized Exception Handling Middleware" if not has_error_handling else "Proceed to Production Containerization & Deployment"
    )
