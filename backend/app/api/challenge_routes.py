from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from app.models.schemas import ChallengeSubmitRequest, ChallengeSubmitResponse
from app.services.code_evaluator import evaluate_challenge_submission, PREDEFINED_CHALLENGES

router = APIRouter(tags=["Interactive Coding Challenges"])

@router.get("/challenges/{challenge_id}")
def get_challenge_detail(challenge_id: str):
    ch = PREDEFINED_CHALLENGES.get(challenge_id)
    if not ch:
        # Generic fallback challenge
        return {
            "id": challenge_id,
            "title": "Interactive Coding Exercise",
            "skill_code": "PY_FUNCS",
            "difficulty": "intermediate",
            "description": "Write a clean function satisfying all boundary cases and test constraints.",
            "starter_code": "def solution(*args):\n    # Write logic here\n    pass",
            "test_cases": [
                {"input": "Sample test 1", "expected": "Expected output"}
            ]
        }
    return ch

@router.post("/challenges/submit", response_model=ChallengeSubmitResponse)
def submit_challenge(req: ChallengeSubmitRequest, x_learner_id: Optional[str] = Header(None)):
    learner_id = x_learner_id or "demo-learner-1"
    result = evaluate_challenge_submission(
        learner_id=learner_id,
        challenge_id=req.challenge_id,
        code_or_answer=req.code_or_answer,
        language=req.language
    )
    return ChallengeSubmitResponse(**result)
