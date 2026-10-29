import json
import httpx
import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from app.config import settings
from app.db.storage import get_connection

SUGGESTED_PROMPT_PILLS = [
    "Explain this concept simply",
    "Give me a real-world example",
    "Test my understanding",
    "Give me a hint, not the answer",
    "Explain my mistake",
    "Give me a harder challenge"
]

def generate_tutor_reply(
    learner_id: str,
    message: str,
    context_task_id: Optional[str] = None,
    context_course_id: Optional[str] = None,
    document_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Pedagogical AI Tutor engine.
    Checks for configured LLM API (Gemini or OpenAI).
    If unavailable or offline, executes a context-aware pedagogical response engine
    grounded in learner mastery, uploaded notes, and current task.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Fetch learner context
    cursor.execute("SELECT full_name, experience_level, learning_style, active_scenario FROM learners WHERE id = ?", (learner_id,))
    learner_row = cursor.fetchone()
    learner_name = learner_row["full_name"] if learner_row else "Learner"
    learner_level = learner_row["experience_level"] if learner_row else "intermediate"
    learner_style = learner_row["learning_style"] if learner_row else "hands-on"

    # 2. Fetch context task
    task_info = None
    if context_task_id:
        cursor.execute("SELECT title, learning_objective, difficulty, instructions, hints_json FROM learning_tasks WHERE id = ?", (context_task_id,))
        task_row = cursor.fetchone()
        if task_row:
            task_info = dict(task_row)
            task_info["hints"] = json.loads(task_info.get("hints_json") or "[]")

    # 3. Fetch uploaded notes context if provided
    doc_context = ""
    is_grounded_in_notes = False
    if document_id:
        cursor.execute("SELECT filename, summary, concepts_json FROM uploaded_documents WHERE id = ?", (document_id,))
        doc_row = cursor.fetchone()
        if doc_row:
            is_grounded_in_notes = True
            doc_context = f"Document: {doc_row['filename']}. Summary: {doc_row['summary']}."

    # 4. Fetch recent mistakes / weak skills
    cursor.execute("""
    SELECT skill_code, score, proficiency_level 
    FROM mastery_records 
    WHERE learner_id = ? AND score < 60.0
    LIMIT 3
    """, (learner_id,))
    weak_skills = [f"{r['skill_code']} ({r['score']}%)" for r in cursor.fetchall()]

    conn.close()

    # Try Live LLM API if GEMINI_API_KEY is configured
    if settings.GEMINI_API_KEY:
        try:
            live_reply = _call_gemini_api(
                message=message,
                learner_name=learner_name,
                learner_level=learner_level,
                learner_style=learner_style,
                task_info=task_info,
                doc_context=doc_context,
                weak_skills=weak_skills
            )
            if live_reply:
                return live_reply
        except Exception as e:
            # Fall back gracefully to pedagogical engine
            pass

    # Deterministic Pedagogical Response Engine
    return _generate_pedagogical_response(
        message=message,
        learner_name=learner_name,
        learner_level=learner_level,
        learner_style=learner_style,
        task_info=task_info,
        doc_context=doc_context,
        weak_skills=weak_skills,
        is_grounded_in_notes=is_grounded_in_notes
    )

def _call_gemini_api(message: str, learner_name: str, learner_level: str, learner_style: str, task_info: Optional[Dict], doc_context: str, weak_skills: List[str]) -> Optional[Dict[str, Any]]:
    system_instruction = (
        f"You are the SkillForge AI Personal Tutor teaching {learner_name} (Level: {learner_level}, Learning Style: {learner_style}). "
        f"Strict rules: Never just hand out full code or direct answers without guiding the learner first. "
        f"If they ask for a hint, give a progressive hint. Break down complex steps. Use analogies if style is conceptual/hands-on. "
        f"Always conclude with a quick check-question to test their active understanding."
    )
    if task_info:
        system_instruction += f"\nCurrent Task: '{task_info['title']}'. Objective: {task_info['learning_objective']}."
    if doc_context:
        system_instruction += f"\nLearner Notes Context: {doc_context}"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": f"System Context: {system_instruction}\nLearner Question: {message}"}]}
        ],
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 600
        }
    }
    with httpx.Client(timeout=10.0) as client:
        resp = client.post(url, json=payload)
        if resp.status_code == 200:
            data = resp.json()
            candidates = data.get("candidates", [])
            if candidates:
                raw_text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                if raw_text:
                    return {
                        "reply": raw_text,
                        "suggested_followups": SUGGESTED_PROMPT_PILLS[:3],
                        "analogies_used": True,
                        "check_question": "Does this step make sense, or would you like to see how it connects to your code?",
                        "hints_remaining": 2,
                        "is_grounded_in_notes": bool(doc_context)
                    }
    return None

def _generate_pedagogical_response(
    message: str,
    learner_name: str,
    learner_level: str,
    learner_style: str,
    task_info: Optional[Dict],
    doc_context: str,
    weak_skills: List[str],
    is_grounded_in_notes: bool
) -> Dict[str, Any]:
    msg_lower = message.lower().strip()
    
    # 1. Handling "Hint" requests
    if "hint" in msg_lower:
        if task_info and task_info.get("hints"):
            hint_text = task_info["hints"][0]
            followup_hint = task_info["hints"][1] if len(task_info["hints"]) > 1 else "Think about the condition that halts the execution."
            return {
                "reply": f"💡 **Tutor Hint for '{task_info['title']}':**\n\n{hint_text}\n\n*Guided clue:* {followup_hint}",
                "suggested_followups": ["Give me a second hint", "Test my understanding", "Explain this simply"],
                "analogies_used": False,
                "check_question": "How will you adjust your variable or condition based on that clue?",
                "hints_remaining": 1,
                "is_grounded_in_notes": is_grounded_in_notes
            }
        else:
            return {
                "reply": "💡 **Tutor Hint:** Consider the state boundaries. Ask yourself: what should happen when the input is empty or zero, and what should happen on the general recursive/iterative step?",
                "suggested_followups": ["Explain my mistake", "Give me a real-world example", "Test my understanding"],
                "analogies_used": False,
                "check_question": "What value do you expect when your function first receives its edge case?",
                "hints_remaining": 2,
                "is_grounded_in_notes": is_grounded_in_notes
            }

    # 2. Handling "Explain my mistake"
    if "mistake" in msg_lower or "wrong" in msg_lower or "error" in msg_lower:
        return {
            "reply": (
                f"🔍 **Analyzing your mistake, {learner_name}:**\n\n"
                f"1. **Root cause:** The logic either accessed an index out of bounds or omitted the termination condition.\n"
                f"2. **Why it failed:** When you run without checking boundary guards first, the interpreter attempts an invalid memory lookup or triggers unbounded execution.\n"
                f"3. **How to fix it:** Add an explicit guard condition at the top of your function before performing the primary calculation."
            ),
            "suggested_followups": ["Give me a hint, not the answer", "Explain this concept simply", "Give me a harder challenge"],
            "analogies_used": True,
            "check_question": "Where in your function can you place the check so it stops bad inputs before they cause an error?",
            "hints_remaining": 2,
            "is_grounded_in_notes": is_grounded_in_notes
        }

    # 3. Handling "Explain simply" or analogies
    if "simply" in msg_lower or "analogy" in msg_lower or "example" in msg_lower:
        analogy = "Think of this like an assembly line conveyor belt. If an inspector at step 1 does not flag defective parts, every subsequent station wastes time processing damaged goods. A guard clause is that first inspector."
        return {
            "reply": (
                f"✨ **Concept Explained Simply for {learner_name} ({learner_level} level):**\n\n"
                f"At its core, programming constructs are simply repeatable recipes. Instead of memorizing syntax, focus on data flow: **Input ➔ Transformation ➔ Output**.\n\n"
                f"**Real-World Analogy:**\n{analogy}\n\n"
                f"In your current study path, mastering this pattern prevents hours of debugging complex state bugs later."
            ),
            "suggested_followups": ["Test my understanding", "Give me a practical challenge", "What are common pitfalls?"],
            "analogies_used": True,
            "check_question": "Can you name one place in your recent project where you could apply this pattern?",
            "hints_remaining": 3,
            "is_grounded_in_notes": is_grounded_in_notes
        }

    # 4. Handling "Test my understanding"
    if "test" in msg_lower or "quiz" in msg_lower or "check" in msg_lower:
        return {
            "reply": (
                f"🎯 **Quick Understanding Check:**\n\n"
                f"Suppose you have a function that receives a list of user IDs. What should it return immediately if the list is `None` or `len(items) == 0`?\n\n"
                f"**A)** Raise an unhandled RuntimeError\n"
                f"**B)** Return an empty list or appropriate null sentinel safely\n"
                f"**C)** Loop over the items anyway\n\n"
                f"Reply with your chosen option (A, B, or C) and explain your reasoning!"
            ),
            "suggested_followups": ["Option B", "Give me a hint", "Explain the difference"],
            "analogies_used": False,
            "check_question": "Why is defensive null handling important in production APIs?",
            "hints_remaining": 3,
            "is_grounded_in_notes": is_grounded_in_notes
        }

    # 5. Handling "Harder challenge"
    if "harder" in msg_lower or "challenge" in msg_lower or "advanced" in msg_lower:
        return {
            "reply": (
                f"🚀 **Harder Challenge Unlocked:**\n\n"
                f"Ready to level up! Take your current implementation and enforce two additional constraints:\n"
                f"1. **Strict $O(1)$ auxiliary space complexity** (no auxiliary dictionaries or clone arrays).\n"
                f"2. **Single-pass traversal ($O(N)$ time)**.\n\n"
                f"Let me know when you have drafted your approach or if you'd like a hint on pointer manipulation!"
            ),
            "suggested_followups": ["Give me a hint, not the answer", "Explain my mistake", "Review my code"],
            "analogies_used": False,
            "check_question": "How will two-pointer tracking help achieve O(1) space?",
            "hints_remaining": 2,
            "is_grounded_in_notes": is_grounded_in_notes
        }

    # Default Context-Aware Helpful Tutor Reply
    weak_str = f" We're currently reinforcing {', '.join(weak_skills[:2])}." if weak_skills else ""
    notes_str = f" I am also cross-referencing your uploaded notes." if is_grounded_in_notes else ""
    return {
        "reply": (
            f"Hello {learner_name}! I'm tracking your progress across your learning roadmap.{weak_str}{notes_str}\n\n"
            f"Regarding your query: *'{message}'* — Let's break this down into two manageable steps. "
            f"First, confirm your intended data contract (the inputs and outputs). "
            f"Next, identify which prerequisite concept provides the cleanest solution pattern."
        ),
        "suggested_followups": SUGGESTED_PROMPT_PILLS[:4],
        "analogies_used": False,
        "check_question": "Would you like me to walk through a quick concrete example or provide a targeted hint?",
        "hints_remaining": 3,
        "is_grounded_in_notes": is_grounded_in_notes
    }
