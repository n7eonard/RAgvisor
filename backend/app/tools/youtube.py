"""YouTube metadata extraction using yt-dlp.

This is a 'tool' in the agentic sense — a function the AI system
can call to gather external data. In Phase 2, this becomes a formal
tool registration for the LangGraph agent.
"""

import logging
import re
from typing import Optional

import yt_dlp

from app.config import get_settings
from app.models.schemas import YouTubeMetadata

logger = logging.getLogger(__name__)

# Regex patterns for YouTube URLs
YT_PATTERNS = [
    r"(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})",
    r"(?:https?://)?youtu\.be/([a-zA-Z0-9_-]{11})",
    r"(?:https?://)?(?:www\.)?youtube\.com/shorts/([a-zA-Z0-9_-]{11})",
    r"(?:https?://)?music\.youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})",
]


def extract_video_id(url: str) -> Optional[str]:
    """Extract the 11-character video ID from various YouTube URL formats."""
    for pattern in YT_PATTERNS:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def fetch_youtube_metadata(url: str) -> YouTubeMetadata:
    """Fetch metadata from a YouTube video without downloading the video.

    Uses yt-dlp in metadata-only mode. This is fast (~1-3s) and doesn't
    require a YouTube API key.
    """
    settings = get_settings()

    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError(f"Could not extract video ID from URL: {url}")

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
        "skip_download": True,
        "socket_timeout": settings.ytdlp_timeout,
        # Only extract metadata, no formats needed
        "format": "best",
        "noplaylist": True,
    }

    logger.info(f"Fetching YouTube metadata for video: {video_id}")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
        except yt_dlp.utils.DownloadError as e:
            raise ValueError(f"Failed to fetch video metadata: {e}")

    return YouTubeMetadata(
        video_id=video_id,
        title=info.get("title", ""),
        uploader=info.get("uploader", info.get("channel", "")),
        description=info.get("description", "")[:2000],  # Cap description length
        duration_seconds=info.get("duration", 0),
        thumbnail_url=info.get("thumbnail"),
        upload_date=info.get("upload_date"),
        view_count=info.get("view_count"),
        tags=info.get("tags", []) or [],
    )
