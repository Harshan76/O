import io
import re
import uuid
import json
from typing import Dict, Any, List, Tuple
from datetime import datetime, timezone
from pypdf import PdfReader
from app.db.storage import get_connection

def extract_text_from_file(file_bytes: bytes, filename: str) -> Tuple[str, int]:
    """Extracts text from PDF or TXT files."""
    filename_lower = filename.lower()
    text = ""
    
    if filename_lower.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(file_bytes))
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    elif filename_lower.endswith(".txt") or filename_lower.endswith(".md"):
        try:
            text = file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            text = file_bytes.decode("latin-1", errors="ignore")
    else:
        raise ValueError("Unsupported file format. Please upload PDF or TXT files.")

    text = text.strip()
    if not text:
        raise ValueError("No readable text found in document.")

    return text, len(text)

def process_document_and_extract(learner_id: str, filename: str, file_bytes: bytes) -> Dict[str, Any]:
    """
    Parses document, extracts key concepts, generates structured summary,
    and persists record to the database.
    """
    text, char_count = extract_text_from_file(file_bytes, filename)
    now = datetime.now(timezone.utc).isoformat()
    doc_id = f"doc-{uuid.uuid4().hex[:8]}"

    # Generate structured summary
    first_paragraph = text.split("\n\n")[0] if "\n\n" in text else text[:350]
    summary = (
        f"Document '{filename}' contains {len(text.split())} words analyzing core computational architecture. "
        f"Key focus: {first_paragraph[:200]}..."
    )

    # Heuristic concept extraction (extract definitions, capitalized terms, bullet points)
    concepts = []
    lines = [line.strip() for line in text.split("\n") if len(line.strip()) > 10]
    
    # Common academic/technical terms extraction
    patterns = [
        r"([A-Z][a-zA-Z\s]{2,25}):\s*(.+)",
        r"([A-Z][a-zA-Z\s]{2,25})\s+is\s+(.+)",
        r"([A-Z][a-zA-Z\s]{2,25})\s+refers to\s+(.+)"
    ]

    for line in lines[:30]:
        for pat in patterns:
            m = re.match(pat, line)
            if m:
                term = m.group(1).strip()
                definition = m.group(2).strip()
                if len(term.split()) <= 4 and len(definition) > 15:
                    concepts.append({
                        "term": term,
                        "definition": definition[:200],
                        "importance": "core" if len(concepts) < 2 else "important",
                        "difficulty": "intermediate"
                    })
                break
        if len(concepts) >= 6:
            break

    # If few concepts matched, synthesize fallback from headings
    if len(concepts) < 3:
        words = [w for w in text.split() if len(w) > 6 and w.isalpha()]
        unique_words = list(dict.fromkeys(words))[:4]
        for w in unique_words:
            concepts.append({
                "term": w.capitalize(),
                "definition": f"Core term identified in {filename} requiring active learner revision.",
                "importance": "important",
                "difficulty": "medium"
            })

    # Save to uploaded_documents in SQLite
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO uploaded_documents (id, learner_id, filename, file_type, file_size, char_count, summary, extracted_text, concepts_json, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (doc_id, learner_id, filename, "application/pdf" if filename.lower().endswith(".pdf") else "text/plain", len(file_bytes), char_count, summary, text, json.dumps(concepts), now))
    
    # Generate initial flashcards for each concept
    for c in concepts:
        fc_id = f"fc-{uuid.uuid4().hex[:8]}"
        cursor.execute("""
        INSERT INTO flashcards (id, learner_id, document_id, skill_code, front, back, confidence, review_count, source_concept, created_at)
        VALUES (?, ?, ?, 'NOTES_GEN', ?, ?, 'learning', 0, ?, ?)
        """, (fc_id, learner_id, doc_id, f"What is {c['term']}?", c['definition'], c['term'], now))

    conn.commit()
    conn.close()

    return {
        "id": doc_id,
        "filename": filename,
        "file_type": "PDF" if filename.lower().endswith(".pdf") else "TXT",
        "file_size": len(file_bytes),
        "char_count": char_count,
        "summary": summary,
        "key_concepts": concepts,
        "preview_snippet": text[:400] + ("..." if len(text) > 400 else "")
    }

def generate_study_tools_from_notes(document_id: str, learner_id: str) -> Dict[str, Any]:
    """Generates flashcards and practice quizzes grounded in the document."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT filename, concepts_json, summary FROM uploaded_documents WHERE id = ?", (document_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise ValueError("Document not found.")

    concepts = json.loads(row["concepts_json"])
    now = datetime.now(timezone.utc).isoformat()

    flashcards = []
    quizzes = []

    for idx, c in enumerate(concepts):
        # Flashcard
        fc_id = f"fc-gen-{uuid.uuid4().hex[:8]}"
        fc_data = {
            "id": fc_id,
            "front": f"Explain the principle of {c['term']}.",
            "back": c["definition"],
            "skill_code": "SMART_NOTES",
            "confidence": "learning",
            "review_count": 0,
            "source_concept": c["term"]
        }
        flashcards.append(fc_data)

        # Quiz Question
        if idx < 4:
            other_defs = [other["definition"] for other in concepts if other["term"] != c["term"]]
            distractor1 = other_defs[0][:90] if len(other_defs) > 0 else "An unrelated hardware acceleration register."
            distractor2 = other_defs[1][:90] if len(other_defs) > 1 else "A deprecated standard library module."
            
            quizzes.append({
                "id": f"q-doc-{idx+1}",
                "skill_id": "SMART_NOTES",
                "prompt": f"Based on your notes '{row['filename']}', how is '{c['term']}' defined?",
                "question_type": "mcq",
                "difficulty": c["difficulty"],
                "options": [
                    {"id": "A", "text": c["definition"]},
                    {"id": "B", "text": distractor1},
                    {"id": "C", "text": distractor2},
                    {"id": "D", "text": "None of the above"}
                ],
                "hints": [f"Review the concept summary for {c['term']}."]
            })

    conn.close()
    return {
        "flashcards": flashcards,
        "generated_quizzes": quizzes
    }
