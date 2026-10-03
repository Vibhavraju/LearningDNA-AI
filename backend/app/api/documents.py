"""Documents API: upload (md/txt/pdf), list and delete documents used for tutor RAG."""

from __future__ import annotations

import io
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.rag import knowledge_base

router = APIRouter(tags=["documents"])
ALLOWED = {".md", ".txt", ".pdf"}
MAX_BYTES = 5 * 1024 * 1024


def _extract_text(filename: str, data: bytes) -> str:
    if filename.lower().endswith(".pdf"):
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise HTTPException(status_code=501, detail="PDF support needs: pip install pypdf") from exc
        try:
            reader = PdfReader(io.BytesIO(data))
            return "\n\n".join((page.extract_text() or "") for page in reader.pages)
        except Exception as exc:
            raise HTTPException(status_code=422, detail=f"Could not read PDF: {exc}") from exc
    return data.decode("utf-8", errors="ignore")


@router.post("/documents")
async def upload_document(user_id: int, file: UploadFile = File(...)):
    name = file.filename or "upload.txt"
    if Path(name).suffix.lower() not in ALLOWED:
        raise HTTPException(status_code=400, detail=f"Unsupported file type. Allowed: {sorted(ALLOWED)}")
    data = await file.read()
    if len(data) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="File too large (max 5 MB)")
    text = _extract_text(name, data).strip()
    if not text:
        raise HTTPException(status_code=422, detail="No text could be extracted from the file")
    doc = knowledge_base.add_document(Path(name).stem.replace("_", " ").title(), text, source=name, owner=user_id)
    return {"document_id": doc["id"], "filename": name, "status": doc["status"], "chunks_created": len(doc["chunks"])}


@router.get("/documents")
def list_documents(user_id: int):
    return {"user_id": user_id, "documents": knowledge_base.list_documents(user_id)}


@router.delete("/documents/{document_id}")
def delete_document(user_id: int, document_id: int):
    if not knowledge_base.delete_document(document_id, owner=user_id):
        raise HTTPException(status_code=404, detail="Document not found")
    return {"document_id": document_id, "status": "deleted"}
