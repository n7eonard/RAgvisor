# Repo Restructure Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Reorganize flat files into a `backend/` + `frontend/` monorepo with Dockerfiles for Railway deployment.

**Architecture:** Monorepo with two independent services. Backend is a FastAPI app under `backend/app/` — existing Python code is moved without modification since imports already use `app.*` prefixes. Frontend is a Vite + React 18 project under `frontend/`. Each service has its own Dockerfile. A docker-compose.yml orchestrates local dev.

**Tech Stack:** Python 3.12, FastAPI, Anthropic SDK, yt-dlp, React 18, Vite, Docker, nginx

---

### Task 1: Configure git identity and create .gitignore

**Files:**
- Create: `.gitignore`

**Step 1: Configure git identity for this worktree**

```bash
cd /Users/usuario/Code/RAgvisor/.claude/worktrees/affectionate-lovelace
git config user.email "usuario@ragvisor.dev"
git config user.name "Usuario"
```

> **Note:** Ask the user for their preferred name/email before running this.

**Step 2: Create .gitignore**

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
dist/
build/
.eggs/
*.egg

# Virtual environments
.venv/
venv/
env/

# Environment variables
.env

# Node
node_modules/
frontend/dist/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Docker
docker-compose.override.yml

# Pytest
.pytest_cache/
htmlcov/
.coverage

# Misc
*.log
```

**Step 3: Commit**

```bash
git add .gitignore
git commit -m "chore: add .gitignore for Python, Node, Docker, IDE files"
```

---

### Task 2: Create backend directory structure and move Python files

**Files:**
- Create: `backend/app/__init__.py`
- Create: `backend/app/models/__init__.py`
- Create: `backend/app/tools/__init__.py`
- Create: `backend/app/agents/__init__.py`
- Create: `backend/tests/__init__.py`
- Move: `main.py` → `backend/app/main.py`
- Move: `config.py` → `backend/app/config.py`
- Move: `schemas.py` → `backend/app/models/schemas.py`
- Move: `youtube.py` → `backend/app/tools/youtube.py`
- Move: `enrichment.py` → `backend/app/agents/enrichment.py`
- Move: `test_phase1.py` → `backend/tests/test_phase1.py`
- Move: `requirements.txt` → `backend/requirements.txt`

**Step 1: Create directory tree**

```bash
mkdir -p backend/app/models backend/app/tools backend/app/agents backend/tests
```

**Step 2: Move Python source files**

```bash
mv main.py backend/app/main.py
mv config.py backend/app/config.py
mv schemas.py backend/app/models/schemas.py
mv youtube.py backend/app/tools/youtube.py
mv enrichment.py backend/app/agents/enrichment.py
mv test_phase1.py backend/tests/test_phase1.py
mv requirements.txt backend/requirements.txt
```

**Step 3: Create `__init__.py` files**

`backend/app/__init__.py` — empty file:
```python
```

`backend/app/models/__init__.py`:
```python
```

`backend/app/tools/__init__.py`:
```python
```

`backend/app/agents/__init__.py`:
```python
```

`backend/tests/__init__.py`:
```python
```

**Step 4: Verify imports resolve**

```bash
cd backend
python -c "from app.config import get_settings; print('config OK')"
python -c "from app.models.schemas import EnrichedTrack; print('schemas OK')"
python -c "from app.tools.youtube import extract_video_id; print('youtube OK')"
python -c "from app.agents.enrichment import process_youtube_url; print('enrichment OK')"
```

Expected: All four print OK. If any fail, check that requirements are installed (`pip install -r requirements.txt`).

**Step 5: Run tests**

```bash
cd backend
pytest tests/ -v
```

Expected: All 12 tests pass.

**Step 6: Commit**

```bash
cd /Users/usuario/Code/RAgvisor/.claude/worktrees/affectionate-lovelace
git add backend/
git commit -m "feat: create backend directory structure and move Python files

Move flat Python files into backend/app/ with proper package layout:
- app/main.py (FastAPI entrypoint)
- app/config.py (settings)
- app/models/schemas.py (Pydantic models)
- app/tools/youtube.py (yt-dlp extraction)
- app/agents/enrichment.py (Claude enrichment)
- tests/test_phase1.py (pytest suite)"
```

---

### Task 3: Create backend Dockerfile and .env.example

**Files:**
- Create: `backend/Dockerfile`
- Create: `backend/.env.example`

**Step 1: Create backend Dockerfile**

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system deps for yt-dlp (ffmpeg optional but useful)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Step 2: Create .env.example**

```env
# Required
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional
LOG_LEVEL=INFO
ENRICHMENT_MODEL=claude-sonnet-4-20250514
ENRICHMENT_MAX_TOKENS=1500
YTDLP_TIMEOUT=15
```

**Step 3: Verify Dockerfile builds**

```bash
cd backend
docker build -t sonicscout-backend .
```

Expected: Build succeeds.

**Step 4: Commit**

```bash
cd /Users/usuario/Code/RAgvisor/.claude/worktrees/affectionate-lovelace
git add backend/Dockerfile backend/.env.example
git commit -m "chore: add backend Dockerfile and .env.example"
```

---

### Task 4: Initialize frontend Vite + React project

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/vite.config.js`
- Create: `frontend/index.html`
- Create: `frontend/src/main.jsx`
- Create: `frontend/src/App.jsx`
- Move: `sonicscout-feed.jsx` → `frontend/src/components/SonicScoutFeed.jsx`

**Step 1: Create frontend directory structure**

```bash
mkdir -p frontend/src/components frontend/public
```

**Step 2: Create package.json**

```json
{
  "name": "sonicscout-frontend",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@types/react": "^18.3.12",
    "@types/react-dom": "^18.3.1",
    "@vitejs/plugin-react": "^4.3.4",
    "vite": "^6.0.0"
  }
}
```

**Step 3: Create vite.config.js**

```js
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
```

**Step 4: Create index.html**

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>SonicScout</title>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
    </style>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

**Step 5: Create src/main.jsx**

```jsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <App />
  </StrictMode>
);
```

**Step 6: Create src/App.jsx**

```jsx
import SonicScoutFeed from "./components/SonicScoutFeed";

export default function App() {
  return <SonicScoutFeed />;
}
```

**Step 7: Move the existing JSX component**

```bash
mv sonicscout-feed.jsx frontend/src/components/SonicScoutFeed.jsx
```

No modifications to the component — it uses mock data and works standalone.

**Step 8: Install dependencies and verify build**

```bash
cd frontend
npm install
npm run build
```

Expected: Build succeeds, `dist/` is created.

**Step 9: Commit**

```bash
cd /Users/usuario/Code/RAgvisor/.claude/worktrees/affectionate-lovelace
git add frontend/
git commit -m "feat: initialize Vite + React frontend with SonicScoutFeed component"
```

---

### Task 5: Create frontend Dockerfile and .env.example

**Files:**
- Create: `frontend/Dockerfile`
- Create: `frontend/.env.example`

**Step 1: Create frontend Dockerfile**

```dockerfile
# Build stage
FROM node:20-alpine AS build

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

# SPA fallback: serve index.html for all routes
RUN echo 'server { \
    listen 80; \
    location / { \
        root /usr/share/nginx/html; \
        try_files $uri /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**Step 2: Create .env.example**

```env
# Backend API URL (set to Railway backend URL in production)
VITE_API_URL=http://localhost:8000
```

**Step 3: Verify Dockerfile builds**

```bash
cd frontend
docker build -t sonicscout-frontend .
```

Expected: Build succeeds.

**Step 4: Commit**

```bash
cd /Users/usuario/Code/RAgvisor/.claude/worktrees/affectionate-lovelace
git add frontend/Dockerfile frontend/.env.example
git commit -m "chore: add frontend Dockerfile (nginx) and .env.example"
```

---

### Task 6: Create docker-compose.yml

**Files:**
- Create: `docker-compose.yml`

**Step 1: Create docker-compose.yml**

```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env
    volumes:
      - ./backend/app:/app/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build: ./frontend
    ports:
      - "5173:80"
    depends_on:
      - backend
```

**Step 2: Commit**

```bash
git add docker-compose.yml
git commit -m "chore: add docker-compose.yml for local development"
```

---

### Task 7: Clean up root files and update README

**Files:**
- Delete: `__init__.py`, `nodeids`, `*.pyc` files at root
- Update: `README.md`

**Step 1: Remove old flat files and artifacts from root**

```bash
rm -f __init__.py __init__.cpython-312.pyc config.cpython-312.pyc schemas.cpython-312.pyc youtube.cpython-312.pyc test_phase1.cpython-312-pytest-9.0.2.pyc nodeids CACHEDIR.TAG
```

> At this point, the only files left at root should be: `README.md`, `.gitignore`, `docker-compose.yml`, plus `backend/`, `frontend/`, `docs/` directories.

**Step 2: Verify clean root**

```bash
ls -la
```

Expected: Only `README.md`, `.gitignore`, `docker-compose.yml`, `.git`, `backend/`, `frontend/`, `docs/`.

**Step 3: Update README.md**

Replace entirely with updated content reflecting the new structure, dev instructions (with and without Docker), and Railway deployment notes. Keep it concise.

Key sections:
- Project description (1-2 lines)
- Architecture diagram (the tree from the design doc)
- Quick Start: Docker (`docker compose up`) and manual (separate terminals)
- Environment variables
- API endpoints (`GET /health`, `POST /enrich`)
- Deployment (Railway: 2 services, root directories, env vars)
- Phase 2 roadmap

**Step 4: Commit**

```bash
git add -A
git commit -m "chore: clean up root files and update README with new structure"
```

---

### Task 8: Final verification

**Step 1: Verify backend starts**

```bash
cd backend
cp .env.example .env
# Edit .env to add a real ANTHROPIC_API_KEY if available, or just test health endpoint
uvicorn app.main:app --port 8000 &
sleep 2
curl http://localhost:8000/health
kill %1
```

Expected: `{"status":"ok","model":"claude-sonnet-4-20250514","has_api_key":false}` (or `true` if key set).

**Step 2: Verify frontend dev server**

```bash
cd frontend
npm run dev &
sleep 3
curl -s http://localhost:5173 | head -5
kill %1
```

Expected: HTML response containing `<div id="root">`.

**Step 3: Verify tests pass**

```bash
cd backend
pytest tests/ -v
```

Expected: All tests pass.

**Step 4: Final commit (if any adjustments)**

```bash
git add -A
git commit -m "chore: final adjustments after verification"
```

---

## Summary

| Task | Description | Files |
|------|-------------|-------|
| 1 | Git config + .gitignore | `.gitignore` |
| 2 | Backend structure + move files | `backend/app/**`, `backend/tests/**` |
| 3 | Backend Dockerfile + .env.example | `backend/Dockerfile`, `backend/.env.example` |
| 4 | Frontend Vite + React init | `frontend/**` |
| 5 | Frontend Dockerfile + .env.example | `frontend/Dockerfile`, `frontend/.env.example` |
| 6 | docker-compose.yml | `docker-compose.yml` |
| 7 | Clean up root + update README | Root cleanup, `README.md` |
| 8 | Final verification | No new files |
