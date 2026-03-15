from pydantic import BaseModel, HttpUrl
from typing import Optional


class YouTubeMetadata(BaseModel):
    """Raw metadata extracted from YouTube."""

    video_id: str
    title: str
    uploader: str
    description: str
    duration_seconds: int
    thumbnail_url: Optional[str] = None
    upload_date: Optional[str] = None
    view_count: Optional[int] = None
    tags: list[str] = []


class TrackIdentification(BaseModel):
    """Parsed artist + track name from YouTube title."""

    artist: str
    track_title: str
    label: Optional[str] = None
    year: Optional[int] = None


class GenreContext(BaseModel):
    """AI-generated genre analysis."""

    genre: str
    sub_genre: Optional[str] = None
    genre_description: str
    scene_origin: str
    related_genres: list[str]
    bpm_range: Optional[str] = None


class ArtistContext(BaseModel):
    """AI-generated artist info."""

    fun_fact: str
    key_artists_to_explore: list[str]
    notable_labels: list[str] = []


class EnrichedTrack(BaseModel):
    """Full enriched track response."""

    # Source
    youtube_url: str
    video_id: str
    thumbnail_url: Optional[str] = None

    # Identification
    artist: str
    track_title: str
    label: Optional[str] = None
    year: Optional[int] = None

    # AI Context
    genre: GenreContext
    artist_context: ArtistContext

    # Metadata
    duration_seconds: int
    view_count: Optional[int] = None


class EnrichRequest(BaseModel):
    """Incoming request to enrich a YouTube URL."""

    youtube_url: str
