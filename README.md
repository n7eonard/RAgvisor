# RAgvisor

AI-powered electronic music discovery feed. Paste a YouTube link, get rich context about the genre, artist, and scene.

## Architecture

```
frontend/          → React app (discovery feed UI)
backend/
  app/
    main.py        → FastAPI entrypoint
    config.py      → Settings & API keys
    models/        → Pydantic schemas
    tools/         → YouTube metadata, web search
    agents/        → AI enrichment (Phase 2: multi-agent)
  tests/           → Pytest test suite
```

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Add your API keys
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Phase 1 (Current)

- YouTube URL → extract metadata (title, artist, description)
- Single LLM call with structured output → genre classification + context
- FastAPI serves enriched track data to React frontend

## Phase 2 (Coming)

- Multi-agent orchestration with LangGraph
- RAG with pgvector for genre knowledge base
- Spotify/Discogs tool integrations
- Evaluation with Opik

## API Keys Required

- `ANTHROPIC_API_KEY` — Claude API for enrichment
- No YouTube API key needed (uses yt-dlp for metadata extraction)
