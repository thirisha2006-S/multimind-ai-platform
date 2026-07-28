"""Configuration management for MultiMind AI Platform."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "MultiMind AI Platform"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: str = "development"

    # API Keys
    openai_api_key: str = ""
    cohere_api_key: str = ""
    tavily_api_key: str = ""

    # AI Models
    openai_model: str = "gpt-4o"
    cohere_model: str = "command"
    tavily_search_model: str = "tavily-search"

    # Database
    database_url: str = "sqlite:///./data/multimind.db"

    # FAISS Vector Store
    faiss_index_path: str = "./data/vector_store/faiss_index"

    # Security
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Data paths
    knowledge_base_path: str = "./data/knowledge_base"
    memory_path: str = "./data/memory"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
