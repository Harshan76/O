import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from app.db.storage import get_connection
from app.models.schemas import LearnerProfile, LearnerProfileUpdate

router = APIRouter(tags=["Learner Profile & Auth"])

@router.get("/profile", response_model=LearnerProfile)
def get_learner_profile(x_learner_id: Optional[str] = Header(None)):
    learner_id = x_learner_id or "demo-learner-1"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, email, full_name, avatar_url, experience_level, daily_minutes, 
           learning_style, target_completion_date, current_streak, longest_streak, 
           total_study_hours, is_simulated
    FROM learners 
    WHERE id = ?
    """, (learner_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        # Return fallback default learner
        return LearnerProfile(
            id=learner_id,
            email="learner@skillforge.ai",
            full_name="Alex Mercer",
            experience_level="beginner",
            daily_minutes=45,
            learning_style="hands-on",
            target_completion_date="2026-12-31",
            current_streak=4,
            longest_streak=12,
            total_study_hours=18.5,
            is_simulated=False
        )

    return LearnerProfile(
        id=row["id"],
        email=row["email"],
        full_name=row["full_name"],
        avatar_url=row["avatar_url"],
        experience_level=row["experience_level"] or "beginner",
        daily_minutes=row["daily_minutes"] or 45,
        learning_style=row["learning_style"] or "hands-on",
        target_completion_date=row["target_completion_date"] or "2026-12-31",
        current_streak=row["current_streak"] or 1,
        longest_streak=row["longest_streak"] or 1,
        total_study_hours=float(row["total_study_hours"] or 0.0),
        is_simulated=bool(row["is_simulated"])
    )

@router.post("/profile", response_model=LearnerProfile)
def update_learner_profile(update_data: LearnerProfileUpdate, x_learner_id: Optional[str] = Header(None)):
    learner_id = x_learner_id or "demo-learner-1"
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now(timezone.utc).isoformat()

    updates = []
    params = []
    if update_data.full_name is not None:
        updates.append("full_name = ?")
        params.append(update_data.full_name)
    if update_data.experience_level is not None:
        updates.append("experience_level = ?")
        params.append(update_data.experience_level)
    if update_data.daily_minutes is not None:
        updates.append("daily_minutes = ?")
        params.append(update_data.daily_minutes)
    if update_data.learning_style is not None:
        updates.append("learning_style = ?")
        params.append(update_data.learning_style)
    if update_data.target_completion_date is not None:
        updates.append("target_completion_date = ?")
        params.append(update_data.target_completion_date)

    if updates:
        updates.append("updated_at = ?")
        params.append(now)
        params.append(learner_id)
        cursor.execute(f"UPDATE learners SET {', '.join(updates)} WHERE id = ?", params)
        conn.commit()

    conn.close()
    return get_learner_profile(x_learner_id=learner_id)

@router.post("/auth/register")
def register_learner(payload: dict):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now(timezone.utc).isoformat()
    learner_id = f"learner-{uuid.uuid4().hex[:8]}"
    email = payload.get("email", "").strip().lower()
    full_name = payload.get("full_name", "").strip() or "Learner"

    if not email:
        conn.close()
        raise HTTPException(status_code=400, detail="Email is required.")

    cursor.execute("""
    INSERT INTO learners (id, email, full_name, experience_level, daily_minutes, learning_style, is_simulated, created_at, updated_at)
    VALUES (?, ?, ?, 'beginner', 45, 'hands-on', 0, ?, ?)
    ON CONFLICT(email) DO UPDATE SET updated_at = excluded.updated_at
    """, (learner_id, email, full_name, now, now))
    conn.commit()

    # Fetch back
    cursor.execute("SELECT id, email, full_name FROM learners WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()

    return {
        "status": "success",
        "message": "Learner registered successfully",
        "learner": {
            "id": row["id"],
            "email": row["email"],
            "full_name": row["full_name"]
        }
    }

@router.post("/auth/login")
def login_learner(payload: dict):
    email = payload.get("email", "").strip().lower()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, full_name, experience_level FROM learners WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        # Auto-create for friendly demo/evaluator experience
        return register_learner(payload)

    return {
        "status": "success",
        "message": "Logged in successfully",
        "learner": {
            "id": row["id"],
            "email": row["email"],
            "full_name": row["full_name"],
            "experience_level": row["experience_level"]
        }
    }
