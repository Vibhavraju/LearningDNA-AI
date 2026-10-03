"""Export service: real PNG and PDF learner identity cards."""

from __future__ import annotations

import io
from typing import Any

from PIL import Image, ImageDraw, ImageFont


def _lines(dna: dict[str, Any]) -> list[tuple[str, str]]:
    traits = dna.get("traits", {})
    return [
        ("Learner type", str(dna.get("learner_type", "n/a"))),
        ("Learning pace", str(dna.get("pace", "n/a"))),
        ("Overall DNA score", f"{dna.get('overall', 0)}/100"),
        ("Retention", f"{dna.get('retention', 0)}/100"),
        ("Consistency", str(dna.get("consistency_label", "n/a"))),
        ("Attention span", f"{dna.get('attention_span_min', 0)} min"),
        ("Best study time", str(traits.get("best_study_time", "n/a"))),
        ("Preferred format", str(traits.get("preferred_format", "n/a"))),
        ("DNA confidence", f"{dna.get('confidence', 0)}%"),
        ("Strengths", ", ".join(dna.get("strong_topics", [])) or "n/a"),
        ("To improve", ", ".join(dna.get("weak_topics", [])) or "n/a"),
    ]


def export_identity_card_png(dna: dict[str, Any], name: str = "Learner") -> bytes:
    w, h = 900, 620
    img = Image.new("RGB", (w, h), "#0f172a")
    d = ImageDraw.Draw(img)
    try:
        title_font = ImageFont.load_default(size=34)
        body_font = ImageFont.load_default(size=22)
    except TypeError:  # very old Pillow
        title_font = body_font = ImageFont.load_default()
    d.rectangle([0, 0, w, 90], fill="#4f46e5")
    d.text((30, 25), f"Learning DNA - {name}", fill="white", font=title_font)
    y = 115
    for label, value in _lines(dna):
        d.text((40, y), label, fill="#94a3b8", font=body_font)
        d.text((280, y), value[:45], fill="#e2e8f0", font=body_font)
        y += 40
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def export_identity_card_pdf(dna: dict[str, Any], name: str = "Learner") -> bytes:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4
    c.setFillColorRGB(0.31, 0.27, 0.9)
    c.rect(0, height - 90, width, 90, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(40, height - 55, f"Learning DNA - {name}")
    y = height - 140
    for label, value in _lines(dna):
        c.setFillColorRGB(0.4, 0.45, 0.55)
        c.setFont("Helvetica", 11)
        c.drawString(40, y, label)
        c.setFillColorRGB(0.05, 0.1, 0.2)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(200, y, value[:70])
        y -= 28
    c.showPage()
    c.save()
    return buf.getvalue()
