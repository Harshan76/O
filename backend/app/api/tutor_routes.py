import json
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Header
from typing import Optional, List
from app.db.storage import get_connection
from app.models.schemas import TutorChatRequest, TutorChatResponse, ChatMessage
from app.services.ai_tutor import generate_tutor_reply

router = APIRouter(tags=["AI Tutor"])

@router.post("/tutor/chat", response_model=TutorChatResponse)
def chat_with_tutor(req: TutorChatRequest, x_learner_id: Optional[str] = Header(None)):
    learner_id = x_learner_id or "demo-learner-1"
    now_str = datetime.now(timezone.utc).strftime("%I:%M %p")
    now_iso = datetime.now(timezone.utc).isoformat()

    # Generate reply
    reply_data = generate_tutor_reply(
        learner_id=learner_id,
        message=req.message,
        context_task_id=req.context_task_id,
        context_course_id=req.context_course_id,
        document_id=req.document_id
    )

    # Persist in tutor_conversations
    conn = get_connection()
    cursor = conn.cursor()
    conv_id = req.conversation_id or f"conv-{learner_id}"

    cursor.execute("SELECT messages_json FROM tutor_conversations WHERE id = ?", (conv_id,))
    row = cursor.fetchone()
    messages = json.loads(row["messages_json"]) if row and row["messages_json"] else []

    # Add learner msg
    messages.append({
        "id": f"msg-{uuid.uuid4().hex[:6]}",
        "sender": "learner",
        "text": req.message,
        "timestamp": now_str,
        "context_task_id": req.context_task_id
    })

    # Add tutor reply
    messages.append({
        "id": f"msg-{uuid.uuid4().hex[:6]}",
        "sender": "tutor",
        "text": reply_data["reply"],
        "timestamp": now_str,
        "suggested_followups": reply_data["suggested_followups"],
        "is_hint": "hint" in req.message.lower(),
        "context_task_id": req.context_task_id
    })

    cursor.execute("""
    INSERT INTO tutor_conversations (id, learner_id, messages_json, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(id) DO UPDATE SET
        messages_json=excluded.messages_json,
        updated_at=excluded.updated_at
    """, (conv_id, learner_id, json.dumps(messages), now_iso, now_iso))

    conn.commit()
    conn.close()

    return TutorChatResponse(**reply_data)

@router.get("/tutor/history", response_model=List[ChatMessage])
def get_tutor_history(x_learner_id: Optional[str] = Header(None)):
    learner_id = x_learner_id or "demo-learner-1"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT messages_json FROM tutor_conversations WHERE learner_id = ? ORDER BY updated_at DESC LIMIT 1", (learner_id,))
    row = cursor.fetchone()
    conn.close()

    if not row or not row["messages_json"]:
        return [
            ChatMessage(
                id="msg-welcome",
                sender="tutor",
                text="Hello! I'm your SkillForge AI Personal Tutor. I'm here to explain concepts, guide you through challenges with progressive hints, and adapt to your pace. What would you like to explore today?",
                timestamp="Just now",
                suggested_followups=["Explain this concept simply", "Give me a real-world example", "Test my understanding"]
            )
        ]

    raw_msgs = json.loads(row["messages_json"])
    return [ChatMessage(**m) for m in raw_msgs]
