# Assumptions

1. The app runs fully in memory by default. PostgreSQL 16 + pgvector (`pgvector/pgvector:pg16`) and Redis are optional
   and only needed for the SQL schema and the Celery worker/beat.
2. There is no login. `user_id` 1-3 are simulated demo learners (`DEMO_MODE=true`); the web app uses a browser-local profile.
3. The mock LLM provider is the default; `anthropic` / `ollama` fall back to it if a key or server is missing.
4. Retrieval for the tutor is TF-IDF (default). Set `EMBEDDING_BACKEND=st` plus `requirements-ml.txt` for sentence-transformers.
5. DKT training uses simulator-generated data and needs PyTorch (optional).
6. CPU only; no GPU required.
7. Document uploads for the tutor: `.md`, `.txt`, `.pdf`, up to 5 MB.
8. All backend timestamps are UTC; the frontend renders local time.
