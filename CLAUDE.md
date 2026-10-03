# Learning DNA AI

## Quick Reference
- Backend: `cd backend && uvicorn app.main:app --reload --port 8000`
- Frontend: `cd frontend && npm run dev`
- Tests: `make test`
- Lint: `make lint`
- DB migrations: `cd backend && alembic upgrade head`
- Seed data: `python -m simulator.seed_demo`

## Architecture
- Frontend: React 18 + TypeScript + Vite + Tailwind CSS + Recharts + TanStack Query + Zustand
- Backend: Python 3.11 + FastAPI + SQLAlchemy 2 (async) + Alembic + Celery
- Database: PostgreSQL 16 (pgvector) + Redis
- ML: scikit-learn, PyTorch (CPU), sentence-transformers
- LLM: provider abstraction (anthropic | ollama | mock)

## Conventions
- Python: type hints everywhere, ruff for linting, Pydantic v2 schemas
- TypeScript: strict mode, ESLint, no `any`
- Small focused modules, comprehensive tests
- Secrets via env vars only — never commit keys
- Branches off main, commit after each phase
