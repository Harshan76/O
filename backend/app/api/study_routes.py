import json
from fastapi import APIRouter, HTTPException, Header, UploadFile, File
from typing import Optional, List
from app.db.storage import get_connection
from app.models.schemas import DocumentUploadResponse, StudyToolsResponse, Flashcard
from app.services.notes_service import process_document_and_extract, generate_study_tools_from_notes

router = APIRouter(tags=["Smart Notes & Study Tools"])

@router.post("/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...), x_learner_id: Optional[str] = Header(None)):
    learner_id = x_learner_id or "demo-learner-1"
    file_bytes = await file.read()
    
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    
    try:
        result = process_document_and_extract(
            learner_id=learner_id,
            filename=file.filename or "notes.txt",
            file_bytes=file_bytes
        )
        return DocumentUploadResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Failed to process document: {str(e)}")

@router.get("/documents")
def get_learner_documents(x_learner_id: Optional[str] = Header(None)):
    learner_id = x_learner_id or "demo-learner-1"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, filename, file_type, file_size, char_count, summary, concepts_json, created_at
    FROM uploaded_documents
    WHERE learner_id = ?
    ORDER BY created_at DESC
    """, (learner_id,))
    rows = cursor.fetchall()
    conn.close()

    docs = []
    for r in rows:
        docs.append({
            "id": r["id"],
            "filename": r["filename"],
            "file_type": r["file_type"],
            "file_size": r["file_size"],
            "char_count": r["char_count"],
            "summary": r["summary"],
            "key_concepts": json.loads(r["concepts_json"] or "[]"),
            "created_at": r["created_at"]
        })
    return docs

@router.post("/study-tools/generate", response_model=StudyToolsResponse)
def generate_study_tools(payload: dict, x_learner_id: Optional[str] = Header(None)):
    learner_id = x_learner_id or "demo-learner-1"
    document_id = payload.get("document_id")
    if not document_id:
        raise HTTPException(status_code=400, detail="document_id is required")

    try:
        tools = generate_study_tools_from_notes(document_id, learner_id)
        return StudyToolsResponse(**tools)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/flashcards", response_model=List[Flashcard])
def get_flashcards(x_learner_id: Optional[str] = Header(None)):
    learner_id = x_learner_id or "demo-learner-1"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, front, back, skill_code, confidence, review_count, source_concept
    FROM flashcards
    WHERE learner_id = ?
    ORDER BY created_at DESC
    """, (learner_id,))
    rows = cursor.fetchall()
    conn.close()

    cards = []
    for r in rows:
        cards.append(Flashcard(
            id=r["id"],
            front=r["front"],
            back=r["back"],
            skill_code=r["skill_code"] or "SMART_NOTES",
            confidence=r["confidence"] or "learning",
            review_count=r["review_count"] or 0,
            source_concept=r["source_concept"]
        ))
    return cards

@router.post("/flashcards/{card_id}/review")
def review_flashcard(card_id: str, payload: dict, x_learner_id: Optional[str] = Header(None)):
    confidence = payload.get("confidence", "learning") # "new", "learning", "mastered"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE flashcards 
    SET confidence = ?, review_count = review_count + 1
    WHERE id = ?
    """, (confidence, card_id))
    conn.commit()
    conn.close()
    return {"status": "success", "card_id": card_id, "confidence": confidence}
