import json
import uuid
from typing import Dict, Any, List, Tuple
from datetime import datetime, timezone
from app.db.storage import get_connection

def calculate_skill_gap_map(learner_id: str) -> Dict[str, Any]:
    """
    Computes a comprehensive skill-gap analysis for the learner:
    - Strong skills (>= 80%)
    - Weak skills (< 50%)
    - In-progress / targeted practice (50% - 79%)
    - Missing prerequisites
    - Validating skills
    - Deterministic calculation breakdown
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get all skills with course info
    cursor.execute("""
    SELECT s.id, s.code, s.name, s.category, s.description, s.difficulty, s.course_id
    FROM skills s
    """)
    all_skills = cursor.fetchall()

    # Get prerequisites
    cursor.execute("SELECT skill_id, prerequisite_code FROM skill_prerequisites")
    prereq_rows = cursor.fetchall()
    prereqs_by_code = {}
    for p in prereq_rows:
        # map skill_id back to code or store
        prereqs_by_code.setdefault(p["skill_id"], []).append(p["prerequisite_code"])

    # Get learner's mastery records
    cursor.execute("""
    SELECT skill_code, score, confidence_score, attempts_count, is_verified, proficiency_level
    FROM mastery_records
    WHERE learner_id = ?
    """, (learner_id,))
    mastery_map = {row["skill_code"]: dict(row) for row in cursor.fetchall()}
    conn.close()

    skill_items = []
    strong_count = 0
    weak_count = 0
    missing_prereqs_count = 0
    validating_count = 0
    total_score = 0.0

    for s in all_skills:
        code = s["code"]
        rec = mastery_map.get(code)
        score = rec["score"] if rec else 0.0
        total_score += score
        
        prereq_codes = prereqs_by_code.get(s["id"], [])
        
        # Check prerequisite status
        has_missing_prereq = False
        for pcode in prereq_codes:
            prec = mastery_map.get(pcode)
            if not prec or prec["score"] < 50.0:
                has_missing_prereq = True
                break

        if has_missing_prereq:
            status = "missing_prereq"
            recommended_action = f"Complete prerequisite ({', '.join(prereq_codes)}) before advancing"
            missing_prereqs_count += 1
        elif score >= 80.0:
            status = "strong"
            recommended_action = "Demonstrated mastery verified — ready for advanced challenge"
            strong_count += 1
        elif 0.0 < score < 50.0:
            status = "weak"
            recommended_action = "Revisit foundational concepts and complete easier challenge"
            weak_count += 1
        elif 50.0 <= score < 80.0:
            status = "validating"
            recommended_action = "Targeted practice required to push into proficient tier"
            validating_count += 1
        else:
            status = "validating"
            recommended_action = "Diagnostic assessment required to establish baseline"
            validating_count += 1

        skill_items.append({
            "code": code,
            "name": s["name"],
            "category": s["category"],
            "description": s["description"],
            "difficulty": s["difficulty"],
            "status": status,
            "score": round(score, 1),
            "prerequisites": prereq_codes,
            "recommended_action": recommended_action
        })

    overall_mastery = round(total_score / max(len(skill_items), 1), 1)

    return {
        "learner_id": learner_id,
        "overall_mastery": overall_mastery,
        "total_skills_mapped": len(skill_items),
        "strong_count": strong_count,
        "weak_count": weak_count,
        "missing_prereqs_count": missing_prereqs_count,
        "validating_count": validating_count,
        "skills": skill_items,
        "calculation_breakdown": {
            "formula": "EMA_score = (latest_attempt * 0.70) + (historical_avg * 0.30)",
            "verification_threshold": "Score >= 80% with minimum 2 validated attempts or practical project pass",
            "adaptation_rules": {
                "below_50": "Revisit prerequisites and offer easier challenge",
                "50_to_79": "Targeted practice on identified sub-skills",
                "above_80": "Promote to harder challenge or practical project"
            }
        }
    }

def evaluate_and_adapt(learner_id: str, assessment_id: str, answers: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Evaluates assessment answers against predefined answer keys and rubrics.
    Updates learner mastery records using deterministic adaptation rules.
    Generates tailored next task recommendations.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, skill_code, prompt, answer_key, explanation, difficulty FROM questions WHERE assessment_id = ?", (assessment_id,))
    question_rows = {row["id"]: row for row in cursor.fetchall()}

    results = []
    correct_count = 0
    total_questions = len(answers)
    now = datetime.now(timezone.utc).isoformat()
    skill_scores = {}

    for ans in answers:
        qid = ans.get("question_id")
        user_val = ans.get("answer", "").strip().upper()
        q = question_rows.get(qid)
        if not q:
            continue

        is_correct = (user_val == q["answer_key"].strip().upper())
        if is_correct:
            correct_count += 1
            score = 100.0
        else:
            score = 0.0

        skill_code = q["skill_code"]
        skill_scores.setdefault(skill_code, []).append(score)

        results.append({
            "question_id": qid,
            "prompt": q["prompt"],
            "user_answer": user_val,
            "correct_answer": q["answer_key"],
            "is_correct": is_correct,
            "score": score,
            "explanation": q["explanation"],
            "skill_code": skill_code,
            "difficulty": q["difficulty"]
        })

    percentage = round((correct_count / max(total_questions, 1)) * 100.0, 1)
    passed = percentage >= 70.0

    # Deterministic adaptation rule
    if percentage < 50.0:
        adaptation_direction = "revisit_prerequisites"
        status_summary = f"Score: {percentage}% — Foundational knowledge gaps detected. Reenrolling in prerequisite review."
    elif 50.0 <= percentage < 80.0:
        adaptation_direction = "targeted_practice"
        status_summary = f"Score: {percentage}% — Good conceptual grasp. Providing targeted practice exercises."
    else:
        adaptation_direction = "advanced_challenge"
        status_summary = f"Score: {percentage}% — High proficiency demonstrated! Advancing to practical implementation challenge."

    # Update Mastery records in DB
    gaps_identified = []
    strengths_identified = []

    for scode, scores in skill_scores.items():
        avg_s = sum(scores) / len(scores)
        # Fetch existing
        cursor.execute("SELECT score, attempts_count FROM mastery_records WHERE learner_id = ? AND skill_code = ?", (learner_id, scode))
        existing = cursor.fetchone()
        
        if existing:
            new_attempts = existing["attempts_count"] + 1
            # EMA: 70% current, 30% past
            new_score = round((avg_s * 0.7) + (existing["score"] * 0.3), 1)
        else:
            new_attempts = 1
            new_score = round(avg_s, 1)

        is_verified = 1 if (new_score >= 80.0 and new_attempts >= 2) else 0
        prof_level = "mastered" if new_score >= 80.0 else ("developing" if new_score >= 50.0 else "novice")

        cursor.execute("""
        INSERT INTO mastery_records (id, learner_id, skill_code, proficiency_level, score, confidence_score, attempts_count, is_verified, last_evaluated_at)
        VALUES (?, ?, ?, ?, ?, 70.0, ?, ?, ?)
        ON CONFLICT(learner_id, skill_code) DO UPDATE SET
            proficiency_level=excluded.proficiency_level,
            score=excluded.score,
            attempts_count=excluded.attempts_count,
            is_verified=excluded.is_verified,
            last_evaluated_at=excluded.last_evaluated_at
        """, (str(uuid.uuid4()), learner_id, scode, prof_level, new_score, new_attempts, is_verified, now))

        if new_score < 50.0:
            gaps_identified.append(scode)
        elif new_score >= 80.0:
            strengths_identified.append(scode)

    # Save assessment attempt
    attempt_id = f"att-{uuid.uuid4().hex[:8]}"
    cursor.execute("""
    INSERT INTO assessment_attempts (id, assessment_id, learner_id, score, max_score, percentage, results_json, mistakes_json, status, completed_at)
    VALUES (?, ?, ?, ?, 100, ?, ?, ?, 'completed', ?)
    """, (attempt_id, assessment_id, learner_id, int(percentage), percentage, json.dumps(results), json.dumps(gaps_identified), now))

    # Log in activity history
    cursor.execute("""
    INSERT INTO learning_activity_history (id, learner_id, activity_type, title, score, details, created_at)
    VALUES (?, ?, 'assessment', 'Diagnostic Assessment Completed', ?, ?, ?)
    """, (str(uuid.uuid4()), learner_id, percentage, f"Completed with {correct_count}/{total_questions} correct ({percentage}%). Adaptation: {adaptation_direction}.", now))

    # Build next recommended task based on adaptation rule
    if adaptation_direction == "revisit_prerequisites":
        recommended_next_task = {
            "title": "Prerequisite Refresher: Foundations & Memory Model",
            "learning_objective": "Reinforce core type declarations and prevent syntax errors.",
            "difficulty": "beginner",
            "estimated_duration": 15,
            "reason": "Diagnostic score fell below 50%; revisiting prerequisites."
        }
    elif adaptation_direction == "targeted_practice":
        recommended_next_task = {
            "title": "Targeted Lab: Edge Cases & Error Boundaries",
            "learning_objective": "Practice handling unexpected inputs and asynchronous boundaries.",
            "difficulty": "intermediate",
            "estimated_duration": 20,
            "reason": "Diagnostic score was 50-79%; providing targeted drill practice."
        }
    else:
        recommended_next_task = {
            "title": "Advanced Engineering Challenge: Production Micro-Service",
            "learning_objective": "Architect full end-to-end implementation with high test coverage.",
            "difficulty": "advanced",
            "estimated_duration": 35,
            "reason": "Demonstrated >= 80% mastery; promoted to advanced challenge."
        }

    conn.commit()
    conn.close()

    return {
        "attempt_id": attempt_id,
        "assessment_id": assessment_id,
        "score": int(percentage),
        "max_score": 100,
        "percentage": percentage,
        "passed": passed,
        "status_summary": status_summary,
        "results": results,
        "skill_gaps_identified": gaps_identified,
        "strengths_identified": strengths_identified,
        "adaptation_direction": adaptation_direction,
        "recommended_next_task": recommended_next_task
    }
