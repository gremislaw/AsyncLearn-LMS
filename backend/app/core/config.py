from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Общие настройки
    APP_NAME: str = "AsyncLearn LMS"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"

    # Безопасность
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 дней

    # Базы данных
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "asynclearn")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")

    MONGO_SERVER: str = os.getenv("MONGO_SERVER", "localhost")
    MONGO_PORT: str = os.getenv("MONGO_PORT", "27017")
    MONGO_DB: str = os.getenv("MONGO_DB", "asynclearn")
    MONGO_USER: Optional[str] = os.getenv("MONGO_USER")
    MONGO_PASSWORD: Optional[str] = os.getenv("MONGO_PASSWORD")

    REDIS_SERVER: str = os.getenv("REDIS_SERVER", "localhost")
    REDIS_PORT: str = os.getenv("REDIS_PORT", "6379")
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    KAFKA_TOPIC_EMAILS: str = os.getenv("KAFKA_TOPIC_EMAILS", "emails")

    # RabbitMQ
    RABBITMQ_SERVER: str = os.getenv("RABBITMQ_SERVER", "localhost")
    RABBITMQ_PORT: str = os.getenv("RABBITMQ_PORT", "5672")
    RABBITMQ_USER: str = os.getenv("RABBITMQ_USER", "guest")
    RABBITMQ_PASSWORD: str = os.getenv("RABBITMQ_PASSWORD", "guest")
    RABBITMQ_QUEUE_VIDEO: str = os.getenv("RABBITMQ_QUEUE_VIDEO", "video_conversion")

    # Email
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = 587
    SMTP_HOST: Optional[str] = os.getenv("SMTP_HOST", "localhost")
    SMTP_USER: Optional[str] = os.getenv("SMTP_USER")
    SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")
    EMAILS_FROM_EMAIL: Optional[str] = os.getenv("EMAILS_FROM_EMAIL", "test@example.com")
    EMAILS_FROM_NAME: Optional[str] = os.getenv("EMAILS_FROM_NAME", "AsyncLearn LMS")

    # AWS S3 (опционально)
    AWS_ACCESS_KEY_ID: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
    S3_BUCKET_NAME: Optional[str] = os.getenv("S3_BUCKET_NAME")
    S3_ENDPOINT_URL: Optional[str] = os.getenv("S3_ENDPOINT_URL")

    # Frontend
    FRONTEND_HOST: str = os.getenv("FRONTEND_HOST", "http://localhost:3000")

    class Config:
        case_sensitive = True

settings = Settings()
