"""Plan API: current plan, regenerate, update task status."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.store import store

router = APIRouter(tags=["plan"])
VALID_STATUS = {"pending", "completed", "skipped"}


@router.get("/plan/{user_id}")
def get_plan(user_id: int):
    return {"user_id": user_id, "tasks": store.user(user_id).plan}


@router.post("/plan/{user_id}")
def generate_new_plan(user_id: int):
    tasks = store.regenerate_plan(user_id)
    return {"status": "plan generated", "user_id": user_id, "tasks": tasks}


@router.patch("/plan/{user_id}/task/{task_id}")
def update_task(user_id: int, task_id: int, status: str = "completed"):
    if status not in VALID_STATUS:
        raise HTTPException(status_code=422, detail=f"status must be one of {sorted(VALID_STATUS)}")
    task = store.update_task(user_id, task_id, status)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task_id": task_id, "status": task["status"], "task": task}
