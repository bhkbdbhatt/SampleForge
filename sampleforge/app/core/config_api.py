"""API-safe settings."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SAMPLEFORGE_", env_file=".env", extra="ignore")

    app_name: str = "sampleforge"
    version: str = "0.1.0"
    environment: str = "development"

    # API
    api_keys: list[str] = []
    rate_limit_enabled: bool = True
    generate_rate_limit: str = "100/minute"
    batch_rate_limit: str = "10/minute"

    # DB/Redis (API may not need redis if using HTTP queue)
    database_url: str = "sqlite+aiosqlite:///./app.db"
    redis_url: str = "redis://localhost:6379/0"

    # Queue
    queue_backend: str = "arq"  # arq or http
    worker_enqueue_url: str | None = None
    worker_enqueue_token: str | None = None

    # Storage
    storage_backend: str = "local"
    local_storage_dir: str = "./var/samples"
    s3_bucket: str | None = None
    s3_endpoint_url: str | None = None
    s3_region: str | None = None

    # Misc
    device: str = "cpu"

    def get_api_keys(self) -> set[str]:
        return set(self.api_keys)


settings = Settings()
