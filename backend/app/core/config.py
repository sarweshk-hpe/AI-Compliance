from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Application
    app_name: str = "Actum AI Compliance Engine"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Database - use localhost when running locally, postgres when in Docker
    database_url: str = "postgresql://actum:actum123@localhost:5432/actum"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # MinIO (Object Storage)
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "actum"
    minio_secret_key: str = "actum123"
    minio_bucket: str = "actum-evidence"
    
    # Security
    jwt_secret_key: str = "your-super-secret-jwt-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
    
    # HMAC Signing (for audit trail)
    hmac_secret_key: str = "your-super-secret-hmac-key-change-in-production"
    
    # AI/LLM Configuration
    nvidia_ai_api_key: str = "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"
    nvidia_ai_model: str = "meta/llama-3.3-70b-instruct"
    ai_temperature: float = 0.2
    ai_top_p: float = 0.7
    ai_enabled: bool = True
    
    # API
    api_v1_prefix: str = "/api/v1"
    
    # CORS
    cors_origins: list = ["http://localhost:3000", "http://frontend:3000"]
    
    # Policy Engine
    default_policy_version: str = "pack-2025-01-01-v1"
    
    # Pattern Detection
    spacy_model: str = "en_core_web_sm"
    
    # Rate Limiting
    rate_limit_per_minute: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()
