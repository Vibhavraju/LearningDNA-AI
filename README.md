# Learning DNA AI

A personalised learning app that works out *how* a student learns and adapts to it.

- **Frontend (React + Vite + Tailwind)** - 20-scenario assessment -> 8-trait Learning DNA, dashboard, 7-day study plan,
  quiz runner (30 questions), AI tutor, resources. Works on its own, state is kept in the browser.
- **Backend (FastAPI)** - the data/ML side: Bayesian Knowledge Tracing, forgetting curve, attention change-point,
  consistency and speed scores, learner-type classifier, recommender, RAG tutor, event ingestion, PNG/PDF DNA card.
  Runs fully in memory with simulated students - no database needed.

The two parts are loosely coupled: the **AI Tutor page** calls the backend (`/api/tutor/chat`, RAG over built-in notes
and uploaded documents) when it is running and falls back to an offline tutor when it is not. The header badge on that
page shows which mode you are in.

## Run it (no Docker, no Postgres, no Redis)

```bash
# terminal 1 - API  (docs: http://localhost:8000/docs)
cd backend
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# terminal 2 - UI   (http://localhost:5173)
cd frontend
npm install
npm run dev
```

On startup the API logs one "Database unavailable" warning if Postgres is not running. That is expected.

## Tests and checks

```bash
cd backend  && python -m pytest tests/ -v      # ML, services, REST + websocket tests
cd frontend && npm test                        # DNA engine / plan engine tests (vitest)
cd frontend && npm run build                   # type-check + production build
cd backend  && python -m ml.evaluate           # BKT next-answer evaluation (see docs/EVALUATION.md)
```

## Optional: full stack with Docker

`docker compose up --build` starts Postgres (pgvector), Redis, the API, Celery worker/beat and the UI.
Use `--profile ollama` to add a local Ollama LLM server.

## Configuration (`.env`, copy from `.env.example`)

| Variable | Meaning |
|----------|---------|
| `LLM_PROVIDER` | `mock` (default, offline) / `anthropic` / `ollama`. Real providers fall back to `mock` on any error. |
| `ANTHROPIC_API_KEY`, `ANTHROPIC_MODEL` | Only for `LLM_PROVIDER=anthropic`. **Never commit a real key.** |
| `DATABASE_URL` | Postgres URL for the SQL schema (alembic). Optional - the API does not need it to run. |
| `DEMO_MODE` | `true` seeds three simulated students (ids 1-3) so every endpoint returns real computed data. |
| `CORS_ORIGINS` | Extra comma-separated origins allowed to call the API. |

## Project layout

```
backend/app/ml/         BKT, forgetting curve, attention, consistency, speed, learner type, DKT (optional PyTorch)
backend/app/services/   features, DNA assembly, recommender, RAG, tutor, narrative, export, LLM providers
backend/app/api/        REST routers + websocket (/ws/{user_id})
backend/app/simulation  student simulator (also used for the demo data and percentile cohort)
backend/ml, simulator   evaluation / DKT training scripts, DB seeding
frontend/src/utils      dnaEngine (scoring), planEngine, streak
frontend/src/pages      Dashboard, MyLearningDNA, StudyPlan, QuizRunner, AITutor, Resources, Settings, Assessment
docs/                   PLAN, ASSUMPTIONS, EVALUATION, VIVA, CHANGELOG
```

## Known limitations (be upfront about these in a viva)

- Backend state is in memory (restart = fresh simulated data). The SQL models and the Alembic migration describe the
  production schema but the endpoints do not read/write them yet.
- There is no authentication; `user_id` is a plain parameter. Fine for a demo, not for production.
- The frontend DNA (8 self-report traits from the assessment) and the backend DNA (5 behavioural dimensions computed from
  study events) are two different models. Only the tutor is connected between them.
- The simulator is the only data source. See `docs/EVALUATION.md` for what has and has not been measured.
