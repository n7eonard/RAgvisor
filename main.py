"""SonicScout API — Phase 1.

Single endpoint that takes a YouTube URL and returns enriched track context.
Run with: uvicorn app.main:app --reload
"""

import logging
import time

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.agents.enrichment import process_youtube_url
from app.config import get_settings
from app.models.schemas import EnrichedTrack, EnrichRequest
from app.tools.youtube import fetch_youtube_metadata

# --- App setup ---

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SonicScout API",
    description="AI-powered electronic music discovery and education",
    version="0.1.0",
)

# CORS for local React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Routes ---


@app.get("/health")
async def health():
    """Health check."""
    settings = get_settings()
    return {
        "status": "ok",
        "model": settings.enrichment_model,
        "has_api_key": bool(settings.anthropic_api_key),
    }


@app.post("/enrich", response_model=EnrichedTrack)
async def enrich_track(request: EnrichRequest):
    """Main endpoint: YouTube URL → enriched track context.

    Pipeline:
    1. Extract metadata from YouTube (yt-dlp)
    2. Identify artist + track name (Claude call #1)
    3. Generate genre + artist context (Claude call #2)
    4. Return structured EnrichedTrack

    Phase 2 will add:
    - RAG retrieval from genre knowledge base
    - Multi-agent orchestration via LangGraph
    - Caching layer for repeated tracks
    - Opik tracing for observability
    """
    start_time = time.time()

    # Step 1: YouTube metadata extraction
    try:
        logger.info(f"Processing YouTube URL: {request.youtube_url}")
        metadata = fetch_youtube_metadata(request.youtube_url)
        logger.info(f"Got metadata: {metadata.title} ({metadata.duration_seconds}s)")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"YouTube extraction failed: {e}")
        raise HTTPException(
            status_code=502,
            detail="Failed to fetch YouTube video metadata. Check the URL and try again.",
        )

    # Step 2+3: AI enrichment
    settings = get_settings()
    if not settings.anthropic_api_key:
        raise HTTPException(
            status_code=503,
            detail="Anthropic API key not configured. Set ANTHROPIC_API_KEY in .env",
        )

    try:
        enriched = process_youtube_url(request.youtube_url, metadata)
    except Exception as e:
        logger.error(f"Enrichment failed: {e}")
        raise HTTPException(
            status_code=502,
            detail=f"AI enrichment failed: {str(e)}",
        )

    elapsed = time.time() - start_time
    logger.info(
        f"Enriched '{enriched.artist} - {enriched.track_title}' "
        f"as {enriched.genre.genre}/{enriched.genre.sub_genre} "
        f"in {elapsed:.1f}s"
    )

    return enriched
