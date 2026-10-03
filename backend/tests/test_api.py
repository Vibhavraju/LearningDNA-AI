import pytest

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402

client = TestClient(app)


def test_root_and_health():
    assert client.get("/").json()["status"] == "running"
    assert client.get("/api/health").json() == {"status": "ok"}


def test_dna_endpoints():
    d = client.get("/api/dna/1").json()
    assert set(d["dimensions"]) == {"learning_speed", "knowledge_retention", "attention_span", "quiz_performance", "learning_consistency"}
    assert "learner_type" in client.get("/api/dna/1/traits").json()
    assert len(client.get("/api/dna/1/history").json()) >= 2
    assert "speed" in client.get("/api/dna/1/explain").json()
    assert client.post("/api/dna/1/recompute").json()["status"] == "recomputed"


def test_plan_complete_flow():
    tasks = client.post("/api/plan/1").json()["tasks"]
    tid = tasks[0]["id"]
    assert client.patch(f"/api/plan/1/task/{tid}").json()["status"] == "completed"
    assert client.get("/api/plan/1").json()["tasks"][0]["status"] == "completed"
    assert client.patch("/api/plan/1/task/9999").status_code == 404


def test_tutor_json_stream_and_history():
    r = client.post("/api/tutor/chat", params={"user_id": 1}, json={"message": "explain recursion"})
    assert r.status_code == 200 and r.json()["response"]
    s = client.post("/api/tutor/chat", params={"user_id": 1, "stream": "true"}, json={"message": "what is SQL"})
    assert "data:" in s.text and '"done": true' in s.text
    assert len(client.get("/api/tutor/history", params={"user_id": 1}).json()["messages"]) >= 4


def test_tutor_uses_client_profile():
    profile = {"pace": "Slow", "preferred_format": "Visual", "attention": 20, "weak_topics": ["Recursion"]}
    r = client.post("/api/tutor/chat", params={"user_id": 1}, json={"message": "explain recursion", "profile": profile})
    assert r.status_code == 200 and "step by step" in r.json()["response"]
    bad = client.post("/api/tutor/chat", params={"user_id": 1}, json={"message": "hi", "profile": {"attention": -5}})
    assert bad.status_code == 422


def test_documents_flow():
    up = client.post("/api/documents", params={"user_id": 1}, files={"file": ("notes.md", b"# Axolotls\n\nAxolotls regenerate limbs.", "text/markdown")})
    assert up.status_code == 200
    doc_id = up.json()["document_id"]
    assert any(d["id"] == doc_id for d in client.get("/api/documents", params={"user_id": 1}).json()["documents"])
    assert client.post("/api/documents", params={"user_id": 1}, files={"file": ("a.exe", b"x", "application/octet-stream")}).status_code == 400
    assert client.delete(f"/api/documents/{doc_id}", params={"user_id": 1}).status_code == 200
    assert client.delete(f"/api/documents/{doc_id}", params={"user_id": 1}).status_code == 404


def test_events_and_export_and_settings():
    ev = [{"user_id": 1, "ts": "2026-10-03T10:00:00Z", "type": "quiz_answer", "topic": "SQL", "payload": {"correct": True}}]
    assert client.post("/api/events", json=ev).json()["accepted"] == 1
    assert client.get("/api/export/dna-card/1?format=png").content[:4] == b"\x89PNG"
    assert client.get("/api/export/dna-card/1?format=pdf").content[:5] == b"%PDF-"
    assert client.get("/api/export/dna-card/1?format=gif").status_code == 400
    assert client.put("/api/settings/1", json={"daily_minutes": 60}).json()["daily_minutes"] == 60


def test_websocket_ping():
    with client.websocket_connect("/ws/1") as ws:
        ws.send_text("ping")
        assert ws.receive_json() == {"event": "pong"}
