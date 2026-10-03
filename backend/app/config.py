"""Central configuration. Reads backend/.env, then ../.env, then real env vars."""

import os
from pathlib import Path

from dotenv import load_dotenv

_BACKEND_DIR = Path(__file__).resolve().parent.parent
for _env in (_BACKEND_DIR / ".env", _BACKEND_DIR.parent / ".env"):
    if _env.exists():
        load_dotenv(_env, override=False)

DEFAULT_SQLITE_URL = f"sqlite+aiosqlite:///{_BACKEND_DIR / 'learning_dna.db'}"


def get_database_url() -> str:
    return os.getenv("DATABASE_URL") or DEFAULT_SQLITE_URL


def get_cors_origins() -> list[str]:
    frontend = os.getenv("FRONTEND_URL", "http://localhost:5173")
    origins = {frontend, "http://localhost:5173", "http://127.0.0.1:5173",
               "http://localhost:3000", "http://127.0.0.1:3000"}
    extra = os.getenv("CORS_ORIGINS", "")
    origins.update(o.strip() for o in extra.split(",") if o.strip())
    return sorted(origins)


DEMO_USER_ID = 1
