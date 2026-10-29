from fastapi import APIRouter, Header
from typing import Optional, List
from app.db.storage import get_connection
from app.models.schemas import ProgressSummary, ActivityItem
from app.services.adaptive_engine import calculate_skill_gap_map

router = APIRouter(tags=["Mastery & Learning History"])

@router.get("/progress/summary", response_model=ProgressSummary)
def get_progress_summary(x_learner_id: Optional[str] = Header(None)):
    learner_id = x_learner_id or "demo-learner-1"
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT email, full_name, current_streak, longest_streak, total_study_hours, is_simulated
    FROM learners 
    WHERE id = ?
    """, (learner_id,))
    l_row = cursor.fetchone()

    cursor.execute("""
    SELECT title FROM learning_goals WHERE learner_id = ? AND status = 'active' ORDER BY created_at DESC LIMIT 1
    """, (learner_id,))
    g_row = cursor.fetchone()
    goal_title = g_row["title"] if g_row else "Python Programming & System Scripting"

    cursor.execute("SELECT COUNT(*) FROM project_submissions WHERE learner_id = ? AND passed = 1", (learner_id,))
    projects_completed = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM learning_activity_history WHERE learner_id = ? AND activity_type = 'challenge'", (learner_id,))
    challenges_completed = cursor.fetchone()[0]

    conn.close()

    skill_profile = calculate_skill_gap_map(learner_id)

    streak = l_row["current_streak"] if l_row else 3
    longest = l_row["longest_streak"] if l_row else 7
    hours = float(l_row["total_study_hours"] if l_row else 14.5)
    is_sim = bool(l_row["is_simulated"]) if l_row else False

    return ProgressSummary(
        learner_id=learner_id,
        goal_title=goal_title,
        current_streak=streak,
        longest_streak=longest,
        total_study_hours=hours,
        overall_mastery=skill_profile["overall_mastery"],
        skills_mastered=skill_profile["strong_count"],
        skills_in_progress=skill_profile["validating_count"] + skill_profile["weak_count"],
        projects_completed=projects_completed,
        challenges_completed=challenges_completed,
        mastery_formula_explanation=(
            "Mastery is computed via an Exponential Moving Average (EMA) weighting the latest demonstrated practical "
            "attempt at 70% and historical consistency at 30%. Verified status is unlocked only after demonstrating >= 80% on 2+ independent challenges."
        ),
        is_simulated=is_sim
    )

@router.get("/progress/history", response_model=List[ActivityItem])
def get_progress_history(x_learner_id: Optional[str] = Header(None)):
    learner_id = x_learner_id or "demo-learner-1"
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, activity_type, title, score, details, created_at
    FROM learning_activity_history
    WHERE learner_id = ?
    ORDER BY created_at DESC
    LIMIT 25
    """, (learner_id,))
    rows = cursor.fetchall()
    conn.close()

    history = []
    for r in rows:
        history.append(ActivityItem(
            id=r["id"],
            activity_type=r["activity_type"],
            title=r["title"],
            score=r["score"],
            timestamp=r["created_at"],
            details=r["details"] or ""
        ))
    return history
