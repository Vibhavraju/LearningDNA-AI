"""Learning DNA AI - FastAPI application entrypoint.

Run:  cd backend && uvicorn app.main:app --reload --port 8000
Docs: http://localhost:8000/docs
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import activity, dna, documents, events, export, plan, settings, tutor, ws
from app.config import get_cors_origins
from app.database import init_db
from app.store import store

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("learning_dna")


@asynccontextmanager
async def lifespan(_: FastAPI):
    db_ok = await init_db()
    store.user(1)  # warm up the demo user (simulate + compute DNA once)
    logger.info("Learning DNA AI started (database: %s). Docs at /docs", "ok" if db_ok else "in-memory only")
    yield


app = FastAPI(title="Learning DNA AI", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Welcome to Learning DNA AI", "status": "running", "docs": "/docs"}


@app.get("/health")
@app.get("/api/health")
def health():
    return {"status": "ok"}


for module in (dna, plan, activity, tutor, documents, events, export, settings):
    app.include_router(module.router, prefix="/api")
app.include_router(ws.router)
