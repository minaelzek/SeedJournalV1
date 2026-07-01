from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    database_url: str = "postgresql+asyncpg://seedjournal:seedjournal_dev@127.0.0.1:5432/seedjournal"
    jwt_secret: str = "dev-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_expire_minutes: int = 15
    apple_client_id: str = "com.seedjournal.app"
    llm_provider: str = "stub"
    openai_api_key: str = ""
    llm_model_fast: str = "stub-fast"
    llm_model_guide: str = "stub-guide"
    embedding_model: str = "stub-embed"
    llm_timeout_sec: int = 30
    cors_origins: str = ""

    @property
    def cors_origin_list(self) -> list[str]:
        if not self.cors_origins.strip():
            return []
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def database_url_sync(self) -> str:
        return self.database_url.replace("postgresql+asyncpg://", "postgresql://", 1)


@lru_cache
def get_settings() -> Settings:
    return Settings()