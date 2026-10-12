"""
Application Configuration
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "AI-Powered DevOps Pipeline"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Server
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "sqlite:///./devops_pipeline.db"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_ENABLED: bool = False
    
    # JWT
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production-12345"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    # ML Configuration
    ML_MODEL_PATH: str = "./ai-engine/models"
    MODEL_RETRAIN_INTERVAL_HOURS: int = 24
    MIN_SAMPLES_FOR_TRAINING: int = 100
    PREDICTION_CONFIDENCE_THRESHOLD: float = 0.7
    
    # Pipeline
    MAX_CONCURRENT_BUILDS: int = 10
    BUILD_TIMEOUT_MINUTES: int = 30
    LOG_RETENTION_DAYS: int = 30
    WORKSPACE_PATH: str = "./workspaces"
    
    # Storage
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE_MB: int = 100
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"
    
    # Metrics
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    
    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = "noreply@devops-pipeline.com"
    EMAIL_ENABLED: bool = False
    
    # Webhooks
    WEBHOOK_SECRET: str = "webhook-secret-key"
    WEBHOOK_TIMEOUT_SECONDS: int = 10
    
    # GitHub
    GITHUB_TOKEN: str = ""
    GITHUB_WEBHOOK_SECRET: str = ""
    
    # Docker
    DOCKER_HOST: str = "unix:///var/run/docker.sock"
    DOCKER_NETWORK: str = "devops_network"
    
    # Kubernetes
    K8S_ENABLED: bool = False
    K8S_NAMESPACE: str = "devops-pipeline"
    KUBECONFIG_PATH: str = "~/.kube/config"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_BURST: int = 100
    
    # Feature Flags
    ENABLE_AI_PREDICTIONS: bool = True
    ENABLE_AUTO_DEPLOY: bool = False
    ENABLE_WEBHOOKS: bool = True
    ENABLE_NOTIFICATIONS: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields from .env


# Create global settings instance
settings = Settings()

# Ensure directories exist
os.makedirs(settings.WORKSPACE_PATH, exist_ok=True)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.ML_MODEL_PATH, exist_ok=True)
os.makedirs("logs", exist_ok=True)
