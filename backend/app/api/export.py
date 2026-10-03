"""Export API: download the learner identity card as PNG or PDF."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Response

from app.services.export import export_identity_card_pdf, export_identity_card_png
from app.store import store

router = APIRouter(tags=["export"])


@router.get("/export/dna-card/{user_id}")
def export_dna_card(user_id: int, format: str = "png"):
    fmt = format.lower()
    if fmt not in {"png", "pdf"}:
        raise HTTPException(status_code=400, detail="format must be 'png' or 'pdf'")
    dna = store.get_dna(user_id)
    name = f"Learner {user_id}"
    if fmt == "pdf":
        data, media = export_identity_card_pdf(dna, name), "application/pdf"
    else:
        data, media = export_identity_card_png(dna, name), "image/png"
    return Response(content=data, media_type=media,
                    headers={"Content-Disposition": f'attachment; filename="learning_dna_card_{user_id}.{fmt}"'})
