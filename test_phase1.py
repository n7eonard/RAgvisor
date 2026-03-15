"""Tests for SonicScout Phase 1.

Run with: pytest tests/ -v
"""

import pytest
from app.tools.youtube import extract_video_id
from app.models.schemas import (
    EnrichRequest,
    YouTubeMetadata,
    TrackIdentification,
    GenreContext,
    ArtistContext,
    EnrichedTrack,
)


# --- YouTube URL parsing ---


class TestExtractVideoId:
    def test_standard_url(self):
        assert (
            extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            == "dQw4w9WgXcQ"
        )

    def test_short_url(self):
        assert extract_video_id("https://youtu.be/dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_music_url(self):
        assert (
            extract_video_id("https://music.youtube.com/watch?v=dQw4w9WgXcQ")
            == "dQw4w9WgXcQ"
        )

    def test_with_extra_params(self):
        assert (
            extract_video_id(
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=120&list=PLtest"
            )
            == "dQw4w9WgXcQ"
        )

    def test_shorts_url(self):
        assert (
            extract_video_id("https://www.youtube.com/shorts/dQw4w9WgXcQ")
            == "dQw4w9WgXcQ"
        )

    def test_no_protocol(self):
        assert (
            extract_video_id("youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"
        )

    def test_invalid_url(self):
        assert extract_video_id("https://example.com/not-youtube") is None

    def test_empty_string(self):
        assert extract_video_id("") is None


# --- Pydantic model validation ---


class TestSchemas:
    def test_enrich_request(self):
        req = EnrichRequest(youtube_url="https://youtu.be/abc12345678")
        assert req.youtube_url == "https://youtu.be/abc12345678"

    def test_youtube_metadata_minimal(self):
        meta = YouTubeMetadata(
            video_id="abc12345678",
            title="Artist - Track",
            uploader="ArtistChannel",
            description="",
            duration_seconds=300,
        )
        assert meta.tags == []
        assert meta.thumbnail_url is None

    def test_genre_context(self):
        gc = GenreContext(
            genre="Techno",
            sub_genre="Dub Techno",
            genre_description="Dub techno merges...",
            scene_origin="Berlin, 1990s",
            related_genres=["Minimal Techno", "Ambient Dub"],
        )
        assert gc.sub_genre == "Dub Techno"
        assert len(gc.related_genres) == 2

    def test_enriched_track_full(self):
        track = EnrichedTrack(
            youtube_url="https://youtu.be/abc",
            video_id="abc",
            artist="Surgeon",
            track_title="La Real",
            genre=GenreContext(
                genre="Techno",
                sub_genre="Birmingham Techno",
                genre_description="Hard, industrial-influenced...",
                scene_origin="Birmingham, UK, early 1990s",
                related_genres=["Industrial Techno"],
            ),
            artist_context=ArtistContext(
                fun_fact="Surgeon is also a trained classical pianist.",
                key_artists_to_explore=["Regis", "Female", "British Murder Boys"],
            ),
            duration_seconds=420,
        )
        assert track.artist == "Surgeon"
        assert track.genre.sub_genre == "Birmingham Techno"
