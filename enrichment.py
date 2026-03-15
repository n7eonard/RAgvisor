"""Track enrichment using Claude.

Phase 1: Single LLM call with structured output (context engineering).
Phase 2: This becomes a LangGraph agent with tool calling, RAG, and
         multi-step reasoning.

This module maps to course concepts:
- Lesson 3: Context Engineering (system prompt design)
- Lesson 4: Structured Outputs (JSON schema enforcement)
- Lesson 5: LLM Workflow Patterns (prompt chaining)
"""

import json
import logging
from typing import Optional

import anthropic

from app.config import get_settings
from app.models.schemas import (
    ArtistContext,
    EnrichedTrack,
    GenreContext,
    TrackIdentification,
    YouTubeMetadata,
)

logger = logging.getLogger(__name__)

# --- System prompts (Context Engineering) ---

TRACK_ID_SYSTEM_PROMPT = """You are an expert electronic music analyst. Given a YouTube video title and metadata, extract the artist name and track title.

Electronic music YouTube titles typically follow patterns like:
- "Artist - Track Title"
- "Artist - Track Title [Label]"
- "Artist - Track Title (Remix)"
- "Artist 'Track Title' (Official Video)"
- Sometimes the uploader/channel name IS the artist

Rules:
- If the title contains " - ", split on the FIRST occurrence
- Strip suffixes like [Official Video], (Official Audio), [Visualizer], etc.
- If a label is mentioned in brackets, extract it
- If you can infer the year from the upload date, include it
- If unsure, use your best judgment based on electronic music conventions

Respond ONLY with valid JSON matching this schema:
{
  "artist": "string",
  "track_title": "string",
  "label": "string or null",
  "year": "integer or null"
}"""

ENRICHMENT_SYSTEM_PROMPT = """You are SonicScout, an AI electronic music expert with deep knowledge of genres, sub-genres, scenes, and artists. Your mission is to educate and delight music enthusiasts with accurate, engaging context about tracks they discover.

You will receive a track's artist, title, and any available YouTube metadata. Generate rich context about the genre and artist.

Guidelines:
- Be SPECIFIC about sub-genres. Don't just say "techno" — identify the specific sub-genre (minimal techno, dub techno, industrial techno, acid techno, etc.)
- Genre descriptions should explain what makes this sub-genre DISTINCT — what does it sound like, what are its signature elements?
- Scene origins should name specific cities, time periods, and key venues/labels
- Fun facts should be genuinely interesting and non-obvious — the kind of thing you'd share at a party
- Related genres should be musically adjacent (not just "other electronic music")
- Key artists to explore should be 3-5 names that fans of this track would likely enjoy
- If you're not confident about specific details, focus on what you know well rather than guessing

Respond ONLY with valid JSON matching this schema:
{
  "genre": {
    "genre": "string (broad genre)",
    "sub_genre": "string or null (specific sub-genre)",
    "genre_description": "string (2-4 sentences explaining the sub-genre)",
    "scene_origin": "string (city/region + time period)",
    "related_genres": ["string", "string", "string"],
    "bpm_range": "string or null (e.g. '128-135')"
  },
  "artist_context": {
    "fun_fact": "string (1-2 sentences, genuinely interesting)",
    "key_artists_to_explore": ["string", "string", "string"],
    "notable_labels": ["string", "string"]
  }
}"""


def _call_claude(system_prompt: str, user_message: str) -> dict:
    """Make a Claude API call and parse JSON response."""
    settings = get_settings()
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    response = client.messages.create(
        model=settings.enrichment_model,
        max_tokens=settings.enrichment_max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )

    raw_text = response.content[0].text.strip()

    # Handle potential markdown code fences
    if raw_text.startswith("```"):
        raw_text = raw_text.split("\n", 1)[1]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3].strip()

    return json.loads(raw_text)


def identify_track(metadata: YouTubeMetadata) -> TrackIdentification:
    """Step 1: Parse artist + track name from YouTube metadata."""
    user_msg = f"""YouTube Video Title: {metadata.title}
Channel/Uploader: {metadata.uploader}
Upload Date: {metadata.upload_date or 'unknown'}
Tags: {', '.join(metadata.tags[:20]) if metadata.tags else 'none'}
Description (first 500 chars): {metadata.description[:500]}"""

    logger.info(f"Identifying track from: {metadata.title}")
    data = _call_claude(TRACK_ID_SYSTEM_PROMPT, user_msg)
    return TrackIdentification(**data)


def enrich_track(
    track_id: TrackIdentification,
    metadata: YouTubeMetadata,
) -> tuple[GenreContext, ArtistContext]:
    """Step 2: Generate rich genre + artist context."""
    user_msg = f"""Artist: {track_id.artist}
Track: {track_id.track_title}
Label: {track_id.label or 'unknown'}
Year: {track_id.year or 'unknown'}

YouTube metadata for additional context:
- Tags: {', '.join(metadata.tags[:20]) if metadata.tags else 'none'}
- Description excerpt: {metadata.description[:500]}
- Channel: {metadata.uploader}"""

    logger.info(f"Enriching track: {track_id.artist} - {track_id.track_title}")
    data = _call_claude(ENRICHMENT_SYSTEM_PROMPT, user_msg)

    genre = GenreContext(**data["genre"])
    artist = ArtistContext(**data["artist_context"])
    return genre, artist


def process_youtube_url(url: str, metadata: YouTubeMetadata) -> EnrichedTrack:
    """Full pipeline: metadata → identify → enrich → structured response.

    This is a simple two-step chain (Lesson 5: LLM Workflow Patterns).
    In Phase 2, this becomes a LangGraph graph with branching,
    tool calls, and RAG retrieval steps.
    """
    # Step 1: Identify artist + track
    track_id = identify_track(metadata)

    # Step 2: Enrich with genre + artist context
    genre_context, artist_context = enrich_track(track_id, metadata)

    # Assemble final response
    return EnrichedTrack(
        youtube_url=url,
        video_id=metadata.video_id,
        thumbnail_url=metadata.thumbnail_url,
        artist=track_id.artist,
        track_title=track_id.track_title,
        label=track_id.label,
        year=track_id.year,
        genre=genre_context,
        artist_context=artist_context,
        duration_seconds=metadata.duration_seconds,
        view_count=metadata.view_count,
    )
