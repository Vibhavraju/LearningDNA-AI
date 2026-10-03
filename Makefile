.PHONY: setup dev up down migrate seed test lint eval backend frontend

setup:
	cp -n .env.example .env || true
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

# Run without Docker (in-memory API + Vite dev server). Use two terminals:
backend:
	cd backend && uvicorn app.main:app --reload --port 8000

frontend:
	cd frontend && npm run dev

# Optional infrastructure (Postgres + Redis) for the SQL schema / Celery workers
dev:
	docker compose up postgres redis -d
	cd backend && alembic upgrade head
	cd backend && python -m simulator.seed_demo
	@echo "Run 'make backend' and 'make frontend' in separate terminals"

up:
	docker compose up --build -d

down:
	docker compose down

migrate:
	cd backend && alembic upgrade head

seed:
	cd backend && python -m simulator.seed_demo

test:
	cd backend && python -m pytest tests/ -v
	cd frontend && npm test

lint:
	cd backend && ruff check .
	cd frontend && npm run lint

eval:
	cd backend && python -m ml.evaluate
