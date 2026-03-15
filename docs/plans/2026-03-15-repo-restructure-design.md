# RAGvisor / SonicScout — Repo Restructure Design

**Date:** 2026-03-15
**Status:** Approved
**Goal:** Restructure flat files exported from a Claude chat into a proper monorepo ready for development and Railway deployment.

## Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Structure | Monorepo plat (backend/ + frontend/) | Standard Railway, imports `app.*` déjà compatibles |
| Python deps | requirements.txt | Simplicité, pas besoin de tooling supplémentaire |
| Frontend | Vite + React 18 | Standard, rapide, bonne DX |
| Deploy | Dockerfiles par service | Parité local/prod, contrôle total du build |
| Platform | Railway (2 services) | Un service backend, un service frontend |

## Target Structure

```
RAGvisor/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              ← FastAPI entrypoint (inchangé)
│   │   ├── config.py            ← Settings + .env (inchangé)
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py       ← Pydantic models (inchangé)
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   └── youtube.py       ← yt-dlp extraction (inchangé)
│   │   └── agents/
│   │       ├── __init__.py
│   │       └── enrichment.py    ← Claude enrichment (inchangé)
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_phase1.py       ← pytest suite (inchangé)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   └── components/
│   │       └── SonicScoutFeed.jsx
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   └── .env.example
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Backend Details

- **No code changes needed** — all Python files already use `from app.xxx import ...` imports.
- `uvicorn app.main:app --reload` launched from `backend/`.
- Dockerfile: `python:3.12-slim`, install requirements, copy app/, expose 8000.
- `.env.example`: `ANTHROPIC_API_KEY=your_key_here`.

## Frontend Details

- Vite + React 18 project initialized with minimal boilerplate.
- `SonicScoutFeed.jsx` moved as-is (mock data, no API connection yet).
- `vite.config.js` proxies `/api` → `http://localhost:8000` for dev.
- Dockerfile: Node build stage → nginx serve stage, expose 80.
- `.env.example`: `VITE_API_URL=http://localhost:8000`.

## Docker Compose (dev)

- `backend`: builds from `backend/`, port 8000, mounts .env, hot-reload.
- `frontend`: builds from `frontend/`, port 5173, depends on backend.
- `docker compose up` starts both services.

## Files to Clean Up

- Remove from root: `main.py`, `config.py`, `schemas.py`, `youtube.py`, `enrichment.py`, `test_phase1.py`, `sonicscout-feed.jsx`, `__init__.py`.
- Remove: `*.pyc` files, `__pycache__` directories, `nodeids`.
- Keep at root: `README.md` (updated), `.gitignore` (new).

## Railway Deployment

- Create 2 services in Railway project, both pointing to this repo.
- Backend service: root directory = `backend/`, uses `backend/Dockerfile`.
- Frontend service: root directory = `frontend/`, uses `frontend/Dockerfile`.
- Set env vars (ANTHROPIC_API_KEY) on backend service.
- Set VITE_API_URL on frontend service pointing to backend's Railway URL.
