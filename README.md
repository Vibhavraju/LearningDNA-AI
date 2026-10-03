# 🧬 Learning DNA AI

**An AI-powered study app that figures out *how* you learn, then adapts your study plan and tutor to match.**

Most e-learning platforms give every student the same lessons in the same order. Learning DNA AI gives each learner a personal **Learning DNA** (a profile of how they take in information, how long they can focus, how well they remember, and how fast they learn) and uses it to build a plan that fits them.

![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Python_3.11+-009688?logo=fastapi&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind-CSS-38BDF8?logo=tailwindcss&logoColor=white)
![Tests](https://img.shields.io/badge/tests-pytest%20%7C%20vitest-brightgreen)

---

## 📌 Table of Contents

- [How it works](#-how-it-works)
- [Features](#-features)
- [The two DNA layers](#-the-two-dna-layers)
- [Tech stack](#-tech-stack)
- [Quick start](#-quick-start)
- [Configuration](#-configuration)
- [Project structure](#-project-structure)
- [Testing and evaluation](#-testing-and-evaluation)
- [Known limitations](#-known-limitations)
- [Roadmap](#-roadmap)
- [Team](#-team)

---

## 🔄 How it works

```
 Take the assessment  ──►  Get your Learning DNA  ──►  Get a 7-day study plan
   (20 scenarios)          (8 traits, DNA code,         (matched to your style
                            archetype)                    and weak topics)
                                                                │
        ▲                                                       ▼
        └────────────  DNA evolves  ◄────  Quizzes + AI Tutor  ◄┘
```

1. **Assess.** Answer 20 short scenario questions about how you study.
2. **Discover.** Receive your DNA code (for example `V-F-M-A`) and an archetype such as *"The Visual Powerhouse"*, with strengths, blind spots and tips.
3. **Plan.** Get a personalised 7-day plan: session lengths, preferred formats, revision for weak topics, and a drill for your weakest learning style.
4. **Practise.** Take quizzes and chat with the AI Tutor. Results feed back into your DNA.

---

## ✨ Features

| Feature | What it does |
|---|---|
| **Learning assessment** | 20 scenario-based questions scored into 8 traits |
| **My Learning DNA** | Radar chart, DNA code, archetype, strengths and blind spots |
| **Dashboard** | Progress rings, streaks, DNA evolution chart |
| **7-day Study Plan** | Auto-generated, adapts to quiz results; progress is kept when the plan is regenerated |
| **Quiz Runner** | 30 questions across 5 subjects (Python, SQL, Statistics, Machine Learning, DSA) |
| **AI Tutor** | RAG-based answers from built-in notes and your own uploaded documents (`.md`, `.txt`, `.pdf`, up to 5 MB) |
| **Resources** | Curated study material per topic |
| **DNA identity card** | Export your profile as PNG or PDF |
| **Live updates** | WebSocket endpoint pushes new data to the UI |
| **Works offline** | The tutor falls back to an offline mode when the backend or an LLM is unavailable |

---

## 🧪 The two DNA layers

The project has two complementary views of a learner.

### 1. Self-report DNA (frontend)
From the 20 assessment answers, eight traits are scored from 0 to 100:

- **Four input styles** (VARK-inspired): Visual, Auditory, Read/Write, Hands-on
- **Four study habits:** Focus, Retention, Pace, Consistency

These produce the DNA code, archetype and study plan. Each finished quiz nudges retention, pace and consistency, so the DNA keeps evolving.

### 2. Behavioural DNA (backend)
Computed from study events using real machine-learning techniques:

| Model | Purpose |
|---|---|
| **Bayesian Knowledge Tracing (BKT)** | Estimates the probability that a learner has mastered each topic |
| **Forgetting curve** `R(t) = e^(-t/S)` | Predicts retention over time and when to revise |
| **Attention change-point detection** | Finds when engagement drops, giving a focus span in minutes |
| **Consistency and speed scores** | Study regularity, and learning speed compared with a simulated cohort |
| **Learner-type classifier** | Nearest-centroid assignment to one of 5 types (e.g. *Steady-Consolidator*, *Burst-Crammer*) |
| **Recommender** | Ranks topics by `0.6 × (1 − mastery) + 0.4 × (1 − retention)` and fits tasks to the attention span |
| **RAG tutor** | TF-IDF retrieval over notes and documents, with a pluggable LLM |
| **DKT (optional)** | LSTM knowledge-tracing model, implemented but not yet evaluated |

The overall behavioural score weights its five dimensions as: retention 30%, speed 25%, consistency 20%, quiz accuracy 15%, attention 10%.

---

## 🛠 Tech stack

**Frontend:** React 18, TypeScript, Vite, Tailwind CSS, Recharts, Zustand, TanStack Query, Framer Motion

**Backend:** Python, FastAPI, NumPy, SciPy, scikit-learn, pandas, Pillow, ReportLab, pypdf

**Optional infrastructure:** PostgreSQL 16 (pgvector), Redis, Celery, Alembic, Docker Compose

**LLM providers:** `mock` (default, offline), `anthropic`, or `ollama`. Real providers fall back to `mock` on any error.

**Quality:** pytest, vitest, ruff, ESLint, GitHub Actions CI

---

## 🚀 Quick start

No Docker, Postgres or Redis needed. You only need **Python 3.11+** and **Node.js 18+**.

**1. Clone the repo**
```bash
git clone https://github.com/Vibhavraju/LearningDNA-AI.git
cd LearningDNA-AI
```

**2. Start the API** (terminal 1)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
API docs: http://localhost:8000/docs

**3. Start the UI** (terminal 2)
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:5173

> 💡 On startup the API may log one *"Database unavailable"* warning. That is expected: the app runs fully in memory by default.

### Optional: full stack with Docker
```bash
docker compose up --build
```
Starts Postgres (pgvector), Redis, the API, the Celery worker and beat, and the UI. Add `--profile ollama` for a local Ollama LLM server.

---

## ⚙️ Configuration

Copy `.env.example` to `.env` and adjust as needed.

| Variable | Meaning |
|---|---|
| `LLM_PROVIDER` | `mock` (default, offline), `anthropic`, or `ollama` |
| `ANTHROPIC_API_KEY`, `ANTHROPIC_MODEL` | Only needed when `LLM_PROVIDER=anthropic` |
| `DATABASE_URL` | Postgres URL for the SQL schema (optional) |
| `DEMO_MODE` | `true` seeds three simulated students (ids 1 to 3) so every endpoint returns real computed data |
| `EMBEDDING_BACKEND` | `hash` (default) or `st` for sentence-transformers (needs `requirements-ml.txt`) |
| `CORS_ORIGINS` | Extra comma-separated origins allowed to call the API |

> ⚠️ **Never commit a real API key or `.env` file.** Only `.env.example` belongs in the repository.

---

## 📂 Project structure

```
Learning-DNA-AI/
├── frontend/
│   └── src/
│       ├── pages/        Dashboard, MyLearningDNA, StudyPlan, QuizRunner, AITutor, Resources, Settings, Assessment
│       ├── utils/        dnaEngine (scoring), planEngine, streak
│       ├── components/   Layout, DNARadar, Ring, Card
│       ├── data/         questions, quiz bank, topics, resources
│       ├── store/        Zustand user store
│       └── tests/        vitest tests
├── backend/
│   ├── app/
│   │   ├── ml/           BKT, forgetting, attention, consistency, speed, learner type, DKT
│   │   ├── services/     features, DNA assembly, recommender, RAG, tutor, export, LLM providers
│   │   ├── api/          REST routers + WebSocket (/ws/{user_id})
│   │   ├── models/       SQLAlchemy models (production schema)
│   │   └── simulation.py Student simulator
│   ├── ml/               Evaluation and DKT training scripts
│   ├── simulator/        Demo data seeding
│   ├── alembic/          Database migrations
│   └── tests/            pytest suite
├── docs/                 PLAN, ASSUMPTIONS, EVALUATION, VIVA, CHANGELOG
├── docker-compose.yml
└── Makefile
```

---

## ✅ Testing and evaluation

```bash
cd backend  && python -m pytest tests/ -v     # ML, services, REST and WebSocket tests
cd frontend && npm test                       # DNA engine and plan engine tests
cd frontend && npm run build                  # type-check and production build
cd backend  && python -m ml.evaluate          # BKT next-answer evaluation
```

Or use the shortcuts: `make test`, `make lint`, `make eval`.

### Measured results (simulated data)

BKT was fitted on the first 70% of each learner's answers and used to predict the remaining 30% (1,512 held-out answers):

| Metric | Result |
|---|---|
| AUC | 0.57 |
| RMSE | 0.48 |
| Accuracy | 64.6% |
| Majority-class baseline accuracy | 66.4% |

**Reading these honestly:** BKT is only slightly better than chance at ranking correct against incorrect answers, and its accuracy is below the baseline. This is likely because the simulator includes forgetting between sessions, which standard BKT cannot model. See [`docs/EVALUATION.md`](docs/EVALUATION.md) for the full discussion. DKT results have not been measured yet, so none are claimed.

---

## ⚠️ Known limitations

- **Simulated data only.** No real learners have used the system, so there is no evidence yet of any effect on learning outcomes.
- **In-memory backend.** Restarting the API resets the simulated data. The SQL models and Alembic migration describe the production schema but endpoints do not use them yet.
- **No authentication.** `user_id` is a plain parameter. Fine for a demo, not for production.
- **Two separate DNA models.** The frontend (8 self-report traits) and backend (5 behavioural dimensions) are not merged. Only the AI Tutor connects them.
- **Not a clinical test.** VARK-style scoring is a study aid, not a diagnostic tool.

---

## 🗺 Roadmap

- [ ] Collect data from real learners and validate the models
- [ ] Add a time-gap / forgetting input to BKT
- [ ] Train and compare DKT against BKT
- [ ] Persist data to PostgreSQL
- [ ] Add authentication
- [ ] Merge the self-report and behavioural DNA into one profile

---

## 👥 Team

| Name | Role |
|---|---|
| P.SriVibhav | Project Lead |
| P.Srivibhav | Product / UX |
| P.Srivibhav | Frontend |
| P.Srivibhav | ML Engineering |
| P.Srivibhav | Backend / AI |
| P.Srivibhav| Evaluation / QA |

---



---

<p align="center">Built to help every student learn in the way that works for them. 🧬</p>
