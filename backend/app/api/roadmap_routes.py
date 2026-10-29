import json
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Header
from typing import Optional, Dict, Any, List
from app.db.storage import get_connection
from app.models.schemas import LearningPathResponse, LearningTask
from app.services.adaptive_engine import calculate_skill_gap_map

router = APIRouter(tags=["Learning Roadmap & Tasks"])

@router.get("/learning-paths/current", response_model=LearningPathResponse)
def get_current_learning_path(x_learner_id: Optional[str] = Header(None)):
    learner_id = x_learner_id or "demo-learner-1"
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, goal_id, title, status, adaptation_reason, progress_percentage
    FROM learning_paths
    WHERE learner_id = ?
    ORDER BY generated_at DESC
    LIMIT 1
    """, (learner_id,))
    path_row = cursor.fetchone()

    if not path_row:
        # Generate default path if none exists
        conn.close()
        return generate_learning_path({}, x_learner_id=learner_id)

    path_id = path_row["id"]
    cursor.execute("""
    SELECT id, path_id, skill_code, title, learning_objective, difficulty, instructions, hints_json, 
           expected_result, evaluation_criteria, estimated_duration, reason_for_recommendation, 
           task_type, status, order_index
    FROM learning_tasks
    WHERE path_id = ?
    ORDER BY order_index ASC
    """, (path_id,))
    task_rows = cursor.fetchall()
    conn.close()

    tasks = []
    for t in task_rows:
        tasks.append(LearningTask(
            id=t["id"],
            path_id=t["path_id"],
            skill_code=t["skill_code"],
            title=t["title"],
            learning_objective=t["learning_objective"],
            difficulty=t["difficulty"],
            instructions=t["instructions"],
            hints=json.loads(t["hints_json"] or "[]"),
            expected_result=t["expected_result"] or "",
            evaluation_criteria=t["evaluation_criteria"] or "",
            estimated_duration=t["estimated_duration"] or 20,
            reason_for_recommendation=t["reason_for_recommendation"] or "",
            task_type=t["task_type"] or "challenge",
            status=t["status"] or "pending",
            order_index=t["order_index"] or 0
        ))

    return LearningPathResponse(
        path_id=path_id,
        learner_id=learner_id,
        goal_id=path_row["goal_id"] or "goal-default",
        title=path_row["title"],
        status=path_row["status"],
        adaptation_reason=path_row["adaptation_reason"] or "Customized based on demonstrated skill mastery",
        tasks=tasks,
        progress_percentage=path_row["progress_percentage"] or 0
    )

@router.post("/learning-paths/generate", response_model=LearningPathResponse)
def generate_learning_path(payload: dict, x_learner_id: Optional[str] = Header(None)):
    learner_id = x_learner_id or "demo-learner-1"
    now = datetime.now(timezone.utc).isoformat()
    path_id = f"path-{uuid.uuid4().hex[:8]}"

    # Assess skills to adapt path
    skill_profile = calculate_skill_gap_map(learner_id)
    skills = skill_profile["skills"]

    tasks_to_create = []
    order = 1

    # Rule 1: Prioritize missing prerequisites and weak skills first
    for s in skills:
        if s["status"] in ["missing_prereq", "weak"]:
            tasks_to_create.append({
                "id": f"task-gen-{uuid.uuid4().hex[:6]}",
                "skill_code": s["code"],
                "title": f"Foundation Drill: {s['name']}",
                "learning_objective": f"Resolve foundational deficits in {s['name']}.",
                "difficulty": "beginner",
                "instructions": f"Study the underlying principles of {s['name']} and complete the targeted exercise.",
                "hints": ["Review lecture notes", "Start with simplified inputs"],
                "expected_result": "Clean execution without prerequisite dependency errors.",
                "evaluation_criteria": "Accurate syntax and logic.",
                "estimated_duration": 15,
                "reason_for_recommendation": f"Demonstrated score ({s['score']}%) indicated critical gap.",
                "task_type": "challenge",
                "status": "pending",
                "order_index": order
            })
            order += 1

    # Rule 2: Next add validating / intermediate skills
    for s in skills:
        if s["status"] == "validating":
            tasks_to_create.append({
                "id": f"task-gen-{uuid.uuid4().hex[:6]}",
                "skill_code": s["code"],
                "title": f"Targeted Practice: {s['name']}",
                "learning_objective": f"Solidify intermediate fluency in {s['name']}.",
                "difficulty": "intermediate",
                "instructions": f"Implement practical pattern applying {s['name']} against edge case tests.",
                "hints": ["Consider boundary values", "Check memory efficiency"],
                "expected_result": "All test assertions pass.",
                "evaluation_criteria": "Correctness and efficiency.",
                "estimated_duration": 25,
                "reason_for_recommendation": f"Score at {s['score']}%; needs targeted validation to reach proficient tier.",
                "task_type": "challenge",
                "status": "pending",
                "order_index": order
            })
            order += 1

    # Rule 3: Add capstone/practical project if strong
    strong_skills = [s for s in skills if s["status"] == "strong"]
    if strong_skills:
        tasks_to_create.append({
            "id": f"task-gen-{uuid.uuid4().hex[:6]}",
            "skill_code": strong_skills[0]["code"],
            "title": f"Practical Application: {strong_skills[0]['name']}",
            "learning_objective": "Integrate mastered concepts into a multi-component practical project.",
            "difficulty": "advanced",
            "instructions": "Build an end-to-end module adhering to the explicit rubric specifications.",
            "hints": ["Keep architecture modular", "Write defensive error guards"],
            "expected_result": "Deployable production artifact meeting all rubric criteria.",
            "evaluation_criteria": "Evaluated against 4 rubric pillars.",
            "estimated_duration": 60,
            "reason_for_recommendation": "High mastery demonstrated across prerequisite skills.",
            "task_type": "project",
            "status": "pending",
            "order_index": order
        })

    # Save to SQLite
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO learning_paths (id, learner_id, goal_id, title, status, adaptation_reason, progress_percentage, generated_at, updated_at)
    VALUES (?, ?, 'goal-active', 'Personalized Adaptive Roadmap', 'active', ?, ?, ?, ?)
    """, (path_id, learner_id, f"Dynamically regenerated based on {len(skills)} mapped skills and {skill_profile['overall_mastery']}% overall mastery.", int(skill_profile["overall_mastery"]), now, now))

    for t in tasks_to_create:
        cursor.execute("""
        INSERT INTO learning_tasks (id, path_id, skill_code, title, learning_objective, difficulty, instructions, hints_json, expected_result, evaluation_criteria, estimated_duration, reason_for_recommendation, task_type, status, order_index, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (t["id"], path_id, t["skill_code"], t["title"], t["learning_objective"], t["difficulty"], t["instructions"], json.dumps(t["hints"]), t["expected_result"], t["evaluation_criteria"], t["estimated_duration"], t["reason_for_recommendation"], t["task_type"], t["status"], t["order_index"], now))

    conn.commit()
    conn.close()

    return get_current_learning_path(x_learner_id=learner_id)

@router.post("/tasks/{task_id}/status")
def update_task_status(task_id: str, payload: dict, x_learner_id: Optional[str] = Header(None)):
    new_status = payload.get("status", "completed")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE learning_tasks SET status = ? WHERE id = ?", (new_status, task_id))
    conn.commit()
    conn.close()
    return {"status": "success", "task_id": task_id, "new_status": new_status}
