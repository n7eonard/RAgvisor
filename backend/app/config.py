from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    anthropic_api_key: str = ""
    log_level: str = "INFO"

    # Claude model for enrichment
    enrichment_model: str = "claude-sonnet-4-20250514"
    enrichment_max_tokens: int = 1500

    # yt-dlp settings
    ytdlp_timeout: int = 15

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
