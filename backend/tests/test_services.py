from datetime import datetime, timezone

from app.services.activity import get_activity_feed
from app.services.dna_service import assemble_dna, compute_dna
from app.services.explain import explain_snapshots
from app.services.export import export_identity_card_pdf, export_identity_card_png
from app.services.ingestion import ingest_events, normalise_event
from app.services.rag import KnowledgeBase
from app.services.recommender import build_gaps, generate_recommendations
from app.services.tutor_service import answer_question
from app.simulation import STUDENT_A, STUDENT_B, generate_events


def test_dna_ranges_and_persona_difference():
    a = compute_dna(generate_events(STUDENT_A, 1), 1)
    b = compute_dna(generate_events(STUDENT_B, 2), 2)
    for d in (a, b):
        for k in ("speed", "retention", "attention", "quiz", "consistency", "overall", "confidence"):
            assert 0 <= d[k] <= 100
    assert a["overall"] > b["overall"]
    assert a["attention_span_min"] > b["attention_span_min"]


def test_dna_empty_user_is_safe():
    d = compute_dna([], 99)
    assert d["overall"] == 0 and d["confidence"] == 0 and d["weak_topics"] == []


def test_assemble_weights_are_normalised():
    d = assemble_dna(80, 80, 80, 80, 80, weights={"speed": 5, "retention": 5, "attention": 5, "quiz": 5, "consistency": 5})
    assert d["overall"] == 80


def test_ingestion_validates():
    now = datetime.now(timezone.utc).isoformat()
    res = ingest_events([{"user_id": 1, "ts": now, "type": "quiz_answer", "topic": "SQL", "payload": {"correct": True}},
                         {"user_id": 1, "type": "quiz_answer"}, {"user_id": 1, "ts": now, "type": "bogus"}])
    assert res["accepted"] == 1 and res["rejected"] == 2
    assert normalise_event({"user_id": "3", "ts": "2026-01-01T10:00:00Z", "type": "session"})["user_id"] == 3


def test_recommendations_fit_budget():
    dna = compute_dna(generate_events(STUDENT_A, 1), 1)
    tasks = generate_recommendations(1, build_gaps(dna), 60, dna["attention_span_min"])
    assert tasks and sum(t["minutes"] for t in tasks) <= 60
    assert [t["rank"] for t in tasks] == list(range(1, len(tasks) + 1))


def test_activity_feed():
    feed = get_activity_feed(generate_events(STUDENT_A, 1), limit=5)
    assert 0 < len(feed) <= 5 and {"title", "detail", "time"} <= set(feed[0])


def test_explain_snapshots():
    a = compute_dna(generate_events(STUDENT_A, 1), 1)
    ex = explain_snapshots(None, a)
    assert set(ex) == {"speed", "retention", "attention", "quiz", "consistency"} and ex["speed"]["delta"] == 0


def test_rag_retrieval_and_ownership():
    kb = KnowledgeBase()
    assert kb.retrieve("what is recursion base case")[0]["document_title"] == "Recursion"
    doc = kb.add_document("My Notes", "Quokkas are small marsupials from Rottnest Island.", owner=5)
    assert kb.retrieve("quokka marsupial", owner=5)[0]["document_title"] == "My Notes"
    assert not kb.retrieve("quokka marsupial", owner=6)
    assert not kb.delete_document(doc["id"], owner=6) and kb.delete_document(doc["id"], owner=5)


def test_tutor_answer_grounded_in_sources():
    answer, sources = answer_question("explain dynamic programming", 1, {"pace": "Fast", "preferred_format": "Visual", "attention": 40, "weak_topics": []})
    assert "subproblems" in answer and "Dynamic Programming" in sources


def test_tutor_adapts_to_supplied_profile():
    slow = {"pace": "Slow", "preferred_format": "Visual", "attention": 20, "weak_topics": ["Recursion"]}
    answer, _ = answer_question("explain recursion", 1, slow)
    assert "step by step" in answer and "20-minute" in answer


def test_exports_are_real_files():
    d = compute_dna(generate_events(STUDENT_A, 1), 1)
    assert export_identity_card_png(d)[:8] == b"\x89PNG\r\n\x1a\n"
    assert export_identity_card_pdf(d)[:5] == b"%PDF-"
