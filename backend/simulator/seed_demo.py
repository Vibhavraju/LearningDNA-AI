"""Seed the SQL database with a demo user, subject and topics.

Run:  cd backend && python -m simulator.seed_demo
(The API itself also seeds simulated events in memory, so this is only needed for the SQL schema.)
"""

from __future__ import annotations

import asyncio
import hashlib
import os
import secrets

from sqlalchemy import select

from app.database import SessionLocal, init_db
from app.models import Subject, Topic, User
from app.simulation import TOPICS


def hash_password(password: str) -> str:
    """PBKDF2-HMAC-SHA256 with a random salt (no passlib/bcrypt dependency)."""
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 200_000).hex()
    return f"pbkdf2${salt}${digest}"


async def seed() -> None:
    print("Seeding demo data...")
    if not await init_db():
        raise SystemExit("Database is not reachable - check DATABASE_URL in .env")
    async with SessionLocal() as session:
        user = (await session.execute(select(User).where(User.email == "alex@demo.com"))).scalar_one_or_none()
        if not user:
            session.add(User(email="alex@demo.com", name="Alex", password_hash=hash_password(os.getenv("DEMO_PASSWORD", "password")), role="student"))
            print("+ user alex@demo.com")
        subject = (await session.execute(select(Subject).where(Subject.name == "AI Fundamentals"))).scalar_one_or_none()
        if not subject:
            subject = Subject(name="AI Fundamentals")
            session.add(subject)
            await session.flush()
            print("+ subject AI Fundamentals")
        existing = {t for (t,) in (await session.execute(select(Topic.name).where(Topic.subject_id == subject.id))).all()}
        for i, name in enumerate(TOPICS):
            if name not in existing:
                session.add(Topic(name=name, subject_id=subject.id, difficulty=round(0.2 + 0.1 * i, 2), order=i))
                print(f"+ topic {name}")
        await session.commit()
    print("Seeding complete.")


if __name__ == "__main__":
    asyncio.run(seed())
