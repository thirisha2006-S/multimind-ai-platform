"""Application configuration settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Multimind AI Platform"
    app_version: str = "0.1.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    environment: str = "development"

    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/multimind"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"

    # ChromaDB (vector store)
    chroma_persist_directory: str = "./data/chroma"

    # Security
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Celery
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
