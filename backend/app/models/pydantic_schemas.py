from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    role: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: float = 0.0

class CourseResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    price: float
    class Config:
        from_attributes = True

class LessonCreate(BaseModel):
    title: str
    video_url: Optional[str] = None
    course_id: int

class LessonResponse(BaseModel):
    id: int
    title: str
    video_url: Optional[str] = None
    course_id: int
    class Config:
        from_attributes = True

class ProgressUpdate(BaseModel):
    watched_seconds: int
    is_completed: bool = False

class ProgressResponse(BaseModel):
    user_id: int
    lesson_id: int
    watched_seconds: int
    is_completed: bool

class VideoUploadRequest(BaseModel):
    video_path: str
    course_id: int
