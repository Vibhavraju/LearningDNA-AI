"""In-memory application state (per user). Seeded with simulated data in DEMO_MODE so every
endpoint returns real, computed results with zero infrastructure."""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from threading import RLock
from typing import Any

from app.config import DEMO_USER_ID
from app.services.dna_service import DEFAULT_WEIGHTS, compute_dna
from app.services.recommender import build_gaps, generate_recommendations

DEFAULT_SETTINGS = {"dna_weights": dict(DEFAULT_WEIGHTS), "daily_minutes": 90,
                    "llm_provider": "mock", "mastery_model": "bkt", "theme": "light"}


class UserState:
    def __init__(self) -> None:
        self.events: list[dict[str, Any]] = []
        self.plan: list[dict[str, Any]] = []
        self.tutor: list[dict[str, Any]] = []
        self.snapshots: list[dict[str, Any]] = []
        self.settings: dict[str, Any] = {**DEFAULT_SETTINGS, "dna_weights": dict(DEFAULT_WEIGHTS)}
        self.dna: dict[str, Any] | None = None


class Store:
    def __init__(self) -> None:
        self._users: dict[int, UserState] = {}
        self._lock = RLock()

    # ---- users / seeding ----
    def user(self, user_id: int) -> UserState:
        with self._lock:
            if user_id not in self._users:
                state = UserState()
                self._users[user_id] = state
                if os.getenv("DEMO_MODE", "true").lower() != "false":
                    self._seed(user_id, state)
            return self._users[user_id]

    def _seed(self, user_id: int, state: UserState) -> None:
        from app.simulation import PERSONAS, generate_events

        persona = PERSONAS[(user_id - DEMO_USER_ID) % len(PERSONAS)]
        state.events = generate_events(persona, user_id, days=28, seed=42 + user_id)
        now = datetime.now(timezone.utc)
        for week in range(1, 5):  # weekly history for the trend chart
            cutoff = now - timedelta(days=7 * (4 - week))
            snap = compute_dna([e for e in state.events if e["ts"] <= cutoff], user_id, cutoff,
                               state.settings["dna_weights"])
            snap["week"] = week
            state.snapshots.append(snap)
        state.dna = state.snapshots[-1]
        state.plan = self._make_plan(user_id, state)

    # ---- events ----
    def add_event(self, user_id: int, event: dict[str, Any]) -> None:
        st = self.user(user_id)
        st.events.append(event)
        st.dna = None  # invalidate cache

    def events(self, user_id: int) -> list[dict[str, Any]]:
        return self.user(user_id).events

    # ---- DNA ----
    def get_dna(self, user_id: int, force: bool = False) -> dict[str, Any]:
        st = self.user(user_id)
        if st.dna is None or force:
            st.dna = compute_dna(st.events, user_id, weights=st.settings["dna_weights"])
        return st.dna

    def recompute_dna(self, user_id: int) -> dict[str, Any]:
        st = self.user(user_id)
        dna = compute_dna(st.events, user_id, weights=st.settings["dna_weights"])
        dna["week"] = (st.snapshots[-1].get("week", 0) + 1) if st.snapshots else 1
        st.snapshots.append(dna)
        st.dna = dna
        return dna

    # ---- plan ----
    def _make_plan(self, user_id: int, state: UserState) -> list[dict[str, Any]]:
        dna = state.dna or compute_dna(state.events, user_id, weights=state.settings["dna_weights"])
        return generate_recommendations(user_id, build_gaps(dna), state.settings["daily_minutes"],
                                        dna.get("attention_span_min"))

    def regenerate_plan(self, user_id: int) -> list[dict[str, Any]]:
        st = self.user(user_id)
        st.dna = compute_dna(st.events, user_id, weights=st.settings["dna_weights"])
        st.plan = self._make_plan(user_id, st)
        return st.plan

    def update_task(self, user_id: int, task_id: int, status: str) -> dict[str, Any] | None:
        for task in self.user(user_id).plan:
            if task["id"] == task_id:
                task["status"] = status
                return task
        return None

    # ---- tutor ----
    def add_message(self, user_id: int, role: str, content: str, sources: list[str] | None = None) -> None:
        msg = {"role": role, "content": content, "ts": datetime.now(timezone.utc).isoformat()}
        if sources:
            msg["sources"] = sources
        self.user(user_id).tutor.append(msg)


store = Store()
