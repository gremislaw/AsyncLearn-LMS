from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class ProgressModel(BaseModel):
    """Модель для хранения прогресса пользователей в MongoDB"""
    user_id: int = Field(..., description="ID пользователя")
    lesson_id: int = Field(..., description="ID урока")
    watched_seconds: int = Field(default=0, description="Количество просмотренных секунд")
    is_completed: bool = Field(default=False, description="Завершен ли урок")
    last_watched_at: datetime = Field(default_factory=datetime.utcnow, description="Время последнего просмотра")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Время создания записи")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "lesson_id": 1,
                "watched_seconds": 120,
                "is_completed": False,
                "last_watched_at": "2023-11-15T10:30:00",
                "created_at": "2023-11-15T10:00:00"
            }
        }

class VideoMetadataModel(BaseModel):
    """Модель для хранения метаданных видео в MongoDB"""
    video_id: str = Field(..., description="Уникальный ID видео")
    lesson_id: int = Field(..., description="ID урока")
    original_filename: str = Field(..., description="Исходное имя файла")
    file_size: int = Field(..., description="Размер файла в байтах")
    duration: int = Field(..., description="Длительность видео в секундах")
    resolution: str = Field(default="1080p", description="Разрешение видео")
    format: str = Field(default="mp4", description="Формат видео")
    s3_url: str = Field(..., description="URL видео в S3")
    thumbnails: list[str] = Field(default_factory=list, description="Список URL превью")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Время загрузки")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Время последнего обновления")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "video_id": "video_123",
                "lesson_id": 1,
                "original_filename": "lesson1.mp4",
                "file_size": 10485760,
                "duration": 600,
                "resolution": "1080p",
                "format": "mp4",
                "s3_url": "s3://asynclearn-videos/video_123.mp4",
                "thumbnails": ["s3://asynclearn-videos/thumbnails/video_123_1.jpg"],
                "created_at": "2023-11-15T10:00:00",
                "updated_at": "2023-11-15T10:00:00"
            }
        }
