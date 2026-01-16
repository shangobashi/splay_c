"""Application settings and configuration."""
from typing import Literal
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

    # Database (SQLite - no Docker needed)
    database_url: str = "sqlite:///./splay.db"

    # JWT
    jwt_secret: str = "your-secret-key-change-in-production-splay-2024"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 15
    jwt_refresh_token_expire_days: int = 7

    # Storage
    storage_type: Literal["local", "s3"] = "local"
    storage_path: str = "./storage"
    s3_bucket: str | None = None
    s3_region: str | None = None

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 1
    environment: Literal["development", "staging", "production"] = "development"

    # External Services (Stubbed for MVP)
    openai_api_key: str = "stub-key-not-used"
    stripe_secret_key: str = "stub-key-not-used"
    stripe_publishable_key: str = "stub-key-not-used"

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == "development"

    @property
    def storage_dir(self) -> Path:
        """Get storage directory as Path object."""
        path = Path(self.storage_path)
        path.mkdir(parents=True, exist_ok=True)
        return path


# Global settings instance
settings = Settings()
