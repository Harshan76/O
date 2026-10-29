import json
from fastapi import APIRouter, HTTPException, Header
from typing import Optional, Dict, Any
from app.db.storage import get_connection
from app.models.schemas import AssessmentStartResponse, AssessmentSubmitRequest, AssessmentSubmitResponse, SkillProfileResponse, AssessmentQuestion
from app.services.adaptive_engine import calculate_skill_gap_map, evaluate_and_adapt

router = APIRouter(tags=["Assessments & Skill-Gap Analysis"])

@router.post("/assessments/start", response_model=AssessmentStartResponse)
def start_assessment(payload: dict, x_learner_id: Optional[str] = Header(None)):
    course_id = payload.get("course_id", "c-python")
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, total_questions FROM assessments WHERE course_id = ? LIMIT 1", (course_id,))
    assessment_row = cursor.fetchone()
    if not assessment_row:
        # Fallback to python diag
        cursor.execute("SELECT id, title, total_questions FROM assessments LIMIT 1")
        assessment_row = cursor.fetchone()

    assessment_id = assessment_row["id"]
    cursor.execute("""
    SELECT id, skill_code, prompt, question_type, difficulty, options_json, hints_json
    FROM questions
    WHERE assessment_id = ?
    """, (assessment_id,))
    q_rows = cursor.fetchall()
    conn.close()

    questions = []
    for r in q_rows:
        questions.append(AssessmentQuestion(
            id=r["id"],
            skill_id=r["skill_code"],
            prompt=r["prompt"],
            question_type=r["question_type"],
            difficulty=r["difficulty"],
            options=json.loads(r["options_json"] or "[]"),
            hints=json.loads(r["hints_json"] or "[]")
        ))

    return AssessmentStartResponse(
        assessment_id=assessment_id,
        title=assessment_row["title"],
        course_id=course_id,
        total_questions=len(questions),
        estimated_minutes=15,
        questions=questions
    )

@router.post("/assessments/submit", response_model=AssessmentSubmitResponse)
def submit_assessment(submission: AssessmentSubmitRequest, x_learner_id: Optional[str] = Header(None)):
    learner_id = x_learner_id or "demo-learner-1"
    raw_answers = [{"question_id": a.question_id, "answer": a.answer} for a in submission.answers]
    result = evaluate_and_adapt(learner_id=learner_id, assessment_id=submission.assessment_id, answers=raw_answers)
    return AssessmentSubmitResponse(**result)

@router.get("/skills/profile", response_model=SkillProfileResponse)
def get_skill_profile(x_learner_id: Optional[str] = Header(None)):
    learner_id = x_learner_id or "demo-learner-1"
    data = calculate_skill_gap_map(learner_id)
    return SkillProfileResponse(**data)
