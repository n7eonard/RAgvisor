# RAgvisor

AI-powered electronic music discovery feed. Paste a YouTube link, get rich context about the genre, artist, and scene.

## Architecture

```
backend/
  app/
    main.py          → FastAPI entrypoint
    config.py        → Settings & API keys
    models/          → Pydantic schemas
    tools/           → YouTube metadata extraction (yt-dlp)
    agents/          → AI enrichment (Claude)
  tests/             → Pytest test suite
  Dockerfile         → Python 3.12-slim + uvicorn
frontend/
  src/
    components/      → React components (SonicScoutFeed)
    App.jsx          → Root component
    main.jsx         → Entry point
  Dockerfile         → Node build + nginx
docker-compose.yml   → Local dev orchestration
```

## Quick Start

### With Docker

```bash
cp backend/.env.example backend/.env  # Add your API keys
docker compose up
```

Backend: http://localhost:8000 | Frontend: http://localhost:5173

### Without Docker

**Backend** (terminal 1):

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your API keys
uvicorn app.main:app --reload
```

**Frontend** (terminal 2):

```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | Yes | — | Claude API key for enrichment |
| `LOG_LEVEL` | No | `INFO` | Logging level |
| `ENRICHMENT_MODEL` | No | `claude-sonnet-4-20250514` | Claude model for enrichment |
| `ENRICHMENT_MAX_TOKENS` | No | `1500` | Max tokens for Claude responses |
| `YTDLP_TIMEOUT` | No | `15` | yt-dlp request timeout (seconds) |

No YouTube API key needed — uses yt-dlp for metadata extraction.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check (returns model info, API key status) |
| `POST` | `/enrich` | YouTube URL → enriched track context |

## Deployment (Railway)

Create two services pointing to this repo:

1. **Backend**: root directory = `backend/`, uses `backend/Dockerfile`. Set `ANTHROPIC_API_KEY` env var.
2. **Frontend**: root directory = `frontend/`, uses `frontend/Dockerfile`. Set `VITE_API_URL` to the backend Railway URL.

## Roadmap

### Phase 1 (Current)

- YouTube URL → extract metadata (title, artist, description)
- Single LLM call with structured output → genre classification + context
- FastAPI serves enriched track data to React frontend

### Phase 2

- Multi-agent orchestration with LangGraph
- RAG with pgvector for genre knowledge base
- Spotify/Discogs tool integrations
- Evaluation with Opik
