import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator

class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "LoL Draft AI Tool"
    DEBUG: bool = False
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1", "*.run.app"]
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://lol-draft-ai-tool.web.app"
    ]
    
    # Riot Games API
    RIOT_API_KEY: str = os.getenv("RIOT_API_KEY", "")
    RIOT_BASE_URL: str = "https://americas.api.riotgames.com"
    RIOT_RATE_LIMIT: int = 100  # requests per 2 minutes
    
    # Google Cloud Platform
    GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "lol-draft-ai-tool")
    FIRESTORE_DATABASE: str = "(default)"
    
    # Cloud SQL (PostgreSQL)
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = os.getenv("DB_NAME", "lol_draft_ai")
    
    # ML/AI Settings
    VERTEX_AI_REGION: str = os.getenv("VERTEX_AI_REGION", "us-central1")
    MODEL_BUCKET: str = os.getenv("MODEL_BUCKET", "lol-draft-ai-models")
    
    # Cache Settings
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL")
    CACHE_TTL: int = 300  # 5 minutes
    
    # Monitoring
    ENABLE_METRICS: bool = True
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @validator("RIOT_API_KEY")
    def validate_riot_api_key(cls, v):
        if not v:
            raise ValueError("RIOT_API_KEY is required")
        return v
    
    @property
    def database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()