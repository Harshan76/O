import uuid
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Header, Query

from app.db.storage import get_connection
from app.db.course_resources import COURSE_LEARNING_RESOURCES
from app.models.schemas import (
    StudentNote,
    StudentNoteCreate,
    StudentNoteUpdate,
    CourseLearningHubResponse
)

router = APIRouter(tags=["Course Learning Hub & Smart Notes"])

@router.get("/courses/{course_id}/resources", response_model=CourseLearningHubResponse)
def get_course_learning_resources(course_id: str):
    """
    Returns topic-wise study notes, concepts, explanations, examples,
    practice questions, and verified educational video resources for the selected course.
    """
    resources = COURSE_LEARNING_RESOURCES.get(course_id)
    if resources:
        return CourseLearningHubResponse(**resources)

    # Fallback to course record from database if not pre-mapped
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, domain, level FROM courses WHERE id = ?", (course_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail=f"Course '{course_id}' not found.")

    fallback_data = {
        "course_id": row["id"],
        "course_title": row["title"],
        "domain": row["domain"],
        "level": row["level"],
        "description": row["description"],
        "diagnostic_assessment_id": "a-python-diag",
        "topics": [
            {
                "id": f"t-{row['id']}-intro",
                "title": f"Foundations of {row['title']}",
                "description": row["description"],
                "estimated_minutes": 20,
                "study_notes": {
                    "introduction": f"Comprehensive introduction to {row['title']}.",
                    "concepts": [
                        {
                            "term": "Core Architecture",
                            "definition": f"Fundamental structural patterns and design paradigms for {row['title']}."
                        }
                    ],
                    "step_by_step": [
                        {
                            "step": "1",
                            "title": "Study Foundations",
                            "description": "Review key concepts and core definitions before practical implementation."
                        }
                    ],
                    "code_example": {
                        "language": "python",
                        "code": "# Foundations example\nprint('SkillForge Learning Track')",
                        "explanation": "Reference implementation demonstrating foundational syntax."
                    },
                    "key_takeaways": [
                        "Complete topic study notes before beginning the assessment.",
                        "Use Smart Notes to record your insights and questions."
                    ],
                    "practice_questions": [
                        {
                            "question": "What is the primary objective of this course?",
                            "answer": row["description"],
                            "explanation": "Review the problem statement and learning goals in the course brief."
                        }
                    ]
                },
                "videos": [
                    {
                        "id": f"v-{row['id']}-1",
                        "title": f"{row['title']} Comprehensive Tutorial",
                        "channel": "freeCodeCamp.org",
                        "embed_url": "https://www.youtube-nocookie.com/embed/rfscVS0vtbw",
                        "watch_url": "https://www.youtube.com/watch?v=rfscVS0vtbw",
                        "search_url": f"https://www.youtube.com/results?search_query={row['title'].replace(' ', '+')}",
                        "duration": "20 mins",
                        "summary": f"Introductory educational lecture covering key topics in {row['title']}."
                    }
                ]
            }
        ]
    }
    return CourseLearningHubResponse(**fallback_data)

@router.get("/courses/{course_id}/notes", response_model=List[StudentNote])
def list_student_notes(
    course_id: str,
    topic_id: Optional[str] = None,
    x_learner_id: Optional[str] = Header(None)
):
    """
    Retrieves all personal smart notes created by the authenticated student
    for the specific course, optionally filtered by topic.
    """
    learner_id = x_learner_id or "demo-learner-1"
    conn = get_connection()
    cursor = conn.cursor()

    if topic_id:
        cursor.execute("""
        SELECT id, learner_id, course_id, topic_id, topic_title, title, content, created_at, updated_at
        FROM student_notes
        WHERE learner_id = ? AND course_id = ? AND topic_id = ?
        ORDER BY updated_at DESC
        """, (learner_id, course_id, topic_id))
    else:
        cursor.execute("""
        SELECT id, learner_id, course_id, topic_id, topic_title, title, content, created_at, updated_at
        FROM student_notes
        WHERE learner_id = ? AND course_id = ?
        ORDER BY updated_at DESC
        """, (learner_id, course_id))

    rows = cursor.fetchall()
    conn.close()

    notes = []
    for r in rows:
        notes.append(StudentNote(
            id=r["id"],
            learner_id=r["learner_id"],
            course_id=r["course_id"],
            topic_id=r["topic_id"],
            topic_title=r["topic_title"],
            title=r["title"],
            content=r["content"],
            created_at=r["created_at"],
            updated_at=r["updated_at"]
        ))
    return notes

@router.post("/courses/{course_id}/notes", response_model=StudentNote)
def create_student_note(
    course_id: str,
    payload: StudentNoteCreate,
    x_learner_id: Optional[str] = Header(None)
):
    """
    Creates a personal smart note for the authenticated student
    associated with the selected course and optional topic.
    """
    learner_id = x_learner_id or "demo-learner-1"
    if not payload.title.strip():
        raise HTTPException(status_code=400, detail="Note title cannot be empty.")
    if not payload.content.strip():
        raise HTTPException(status_code=400, detail="Note content cannot be empty.")

    note_id = f"note-{uuid.uuid4().hex[:12]}"
    now = datetime.now(timezone.utc).isoformat()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO student_notes (id, learner_id, course_id, topic_id, topic_title, title, content, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (note_id, learner_id, course_id, payload.topic_id, payload.topic_title, payload.title.strip(), payload.content.strip(), now, now))
    conn.commit()
    conn.close()

    return StudentNote(
        id=note_id,
        learner_id=learner_id,
        course_id=course_id,
        topic_id=payload.topic_id,
        topic_title=payload.topic_title,
        title=payload.title.strip(),
        content=payload.content.strip(),
        created_at=now,
        updated_at=now
    )

@router.put("/courses/{course_id}/notes/{note_id}", response_model=StudentNote)
def update_student_note(
    course_id: str,
    note_id: str,
    payload: StudentNoteUpdate,
    x_learner_id: Optional[str] = Header(None)
):
    """
    Updates an existing student note. Ensures the student owns the note.
    """
    learner_id = x_learner_id or "demo-learner-1"
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, content, topic_id, topic_title, created_at FROM student_notes WHERE id = ? AND learner_id = ? AND course_id = ?", (note_id, learner_id, course_id))
    existing = cursor.fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Note not found or does not belong to the current learner.")

    new_title = payload.title.strip() if payload.title is not None else existing["title"]
    new_content = payload.content.strip() if payload.content is not None else existing["content"]
    new_topic_id = payload.topic_id if payload.topic_id is not None else existing["topic_id"]
    new_topic_title = payload.topic_title if payload.topic_title is not None else existing["topic_title"]
    now = datetime.now(timezone.utc).isoformat()

    cursor.execute("""
    UPDATE student_notes
    SET title = ?, content = ?, topic_id = ?, topic_title = ?, updated_at = ?
    WHERE id = ? AND learner_id = ?
    """, (new_title, new_content, new_topic_id, new_topic_title, now, note_id, learner_id))
    conn.commit()
    conn.close()

    return StudentNote(
        id=note_id,
        learner_id=learner_id,
        course_id=course_id,
        topic_id=new_topic_id,
        topic_title=new_topic_title,
        title=new_title,
        content=new_content,
        created_at=existing["created_at"],
        updated_at=now
    )

@router.delete("/courses/{course_id}/notes/{note_id}")
def delete_student_note(
    course_id: str,
    note_id: str,
    x_learner_id: Optional[str] = Header(None)
):
    """
    Deletes an existing student note with ownership verification.
    """
    learner_id = x_learner_id or "demo-learner-1"
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM student_notes WHERE id = ? AND learner_id = ? AND course_id = ?", (note_id, learner_id, course_id))
    existing = cursor.fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Note not found or does not belong to the current learner.")

    cursor.execute("DELETE FROM student_notes WHERE id = ? AND learner_id = ?", (note_id, learner_id))
    conn.commit()
    conn.close()

    return {"status": "success", "deleted_note_id": note_id, "message": "Note deleted successfully."}
