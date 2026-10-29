import json
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Header
from typing import List, Optional
from app.db.storage import get_connection
from app.models.schemas import Course, LearningGoal, LearningGoalCreate

router = APIRouter(tags=["Courses & Learning Goals"])

@router.get("/courses", response_model=List[Course])
def list_courses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, slug, title, description, domain, level, modules_json FROM courses WHERE is_active = 1")
    rows = cursor.fetchall()
    conn.close()

    courses = []
    for r in rows:
        courses.append(Course(
            id=r["id"],
            slug=r["slug"],
            title=r["title"],
            description=r["description"],
            domain=r["domain"],
            level=r["level"],
            modules=json.loads(r["modules_json"] or "[]")
        ))
    return courses

@router.get("/learning-goals", response_model=List[LearningGoal])
def get_learning_goals(x_learner_id: Optional[str] = Header(None)):
    learner_id = x_learner_id or "demo-learner-1"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, learner_id, title, domain, target_outcome, target_date, status, progress_percentage
    FROM learning_goals
    WHERE learner_id = ?
    """, (learner_id,))
    rows = cursor.fetchall()
    conn.close()

    goals = []
    for r in rows:
        goals.append(LearningGoal(
            id=r["id"],
            learner_id=r["learner_id"],
            title=r["title"],
            domain=r["domain"],
            target_outcome=r["target_outcome"],
            target_date=r["target_date"],
            status=r["status"],
            progress_percentage=r["progress_percentage"]
        ))
    return goals

@router.post("/learning-goals", response_model=LearningGoal)
def create_learning_goal(goal_in: LearningGoalCreate, x_learner_id: Optional[str] = Header(None)):
    learner_id = x_learner_id or "demo-learner-1"
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now(timezone.utc).isoformat()
    goal_id = f"goal-{uuid.uuid4().hex[:8]}"

    # Update learner onboarding preferences
    cursor.execute("""
    UPDATE learners 
    SET experience_level = ?, daily_minutes = ?, learning_style = ?, target_completion_date = ?, updated_at = ?
    WHERE id = ?
    """, (goal_in.experience_level, goal_in.daily_minutes, goal_in.learning_style, goal_in.target_date, now, learner_id))

    # Insert goal
    cursor.execute("""
    INSERT INTO learning_goals (id, learner_id, title, domain, target_outcome, target_date, status, progress_percentage, created_at)
    VALUES (?, ?, ?, ?, ?, ?, 'active', 0, ?)
    """, (goal_id, learner_id, goal_in.title, goal_in.domain, goal_in.target_outcome, goal_in.target_date, now))
    
    conn.commit()
    conn.close()

    return LearningGoal(
        id=goal_id,
        learner_id=learner_id,
        title=goal_in.title,
        domain=goal_in.domain,
        target_outcome=goal_in.target_outcome,
        target_date=goal_in.target_date,
        status="active",
        progress_percentage=0
    )
