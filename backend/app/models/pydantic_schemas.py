from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from app.models.sql_models import UserRole

# Базовые схемы
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

# Схемы для пользователей
class UserBase(BaseSchema):
    username: str
    email: EmailStr
    role: UserRole = UserRole.student

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseSchema):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

class UserLogin(BaseSchema):
    username: str
    password: str

class Token(BaseSchema):
    access_token: str
    token_type: str

# Схемы для курсов
class CourseBase(BaseSchema):
    title: str
    description: Optional[str] = None
    price: int = 0
    is_active: bool = True

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    is_active: Optional[bool] = None

class CourseResponse(CourseBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class CourseWithLessons(CourseResponse):
    lessons: List['LessonResponse'] = []

# Схемы для уроков
class LessonBase(BaseSchema):
    title: str
    description: Optional[str] = None
    video_url: Optional[str] = None
    duration: Optional[int] = None
    order: int = 1
    is_active: bool = True

class LessonCreate(LessonBase):
    course_id: int

class LessonUpdate(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    video_url: Optional[str] = None
    duration: Optional[int] = None
    order: Optional[int] = None
    is_active: Optional[bool] = None

class LessonResponse(LessonBase):
    id: int
    course_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

# Схемы для прогресса
class ProgressBase(BaseSchema):
    watched_seconds: int = 0
    is_completed: bool = False

class ProgressCreate(ProgressBase):
    lesson_id: int

class ProgressUpdate(BaseSchema):
    watched_seconds: Optional[int] = None
    is_completed: Optional[bool] = None

class ProgressResponse(ProgressBase):
    id: int
    user_id: int
    lesson_id: int
    last_watched_at: datetime

# Схемы для записей
class EnrollmentBase(BaseSchema):
    expires_at: Optional[datetime] = None

class EnrollmentCreate(EnrollmentBase):
    course_id: int

class EnrollmentResponse(EnrollmentBase):
    id: int
    user_id: int
    course_id: int
    enrolled_at: datetime

# Схемы для оплаты
class PaymentCreate(BaseSchema):
    course_id: int
    payment_method: str

class PaymentResponse(BaseSchema):
    id: int
    user_id: int
    course_id: int
    amount: int
    status: str
    created_at: datetime

# Схемы для email
class EmailSchema(BaseSchema):
    to: str
    subject: str
    body: str

# Схемы для видео конвертации
class VideoConversionSchema(BaseSchema):
    video_id: str
    video_path: str
    output_format: str = "mp4"
