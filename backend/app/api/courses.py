from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.core import database
from app.models.sql_models import Course, Lesson, User, Enrollment
from app.models.pydantic_schemas import (
    CourseCreate, CourseUpdate, CourseResponse, CourseWithLessons,
    LessonCreate, LessonUpdate, LessonResponse,
    EnrollmentCreate, EnrollmentResponse
)
from app.services.course_service import CourseService
from app.services.lesson_service import LessonService
from app.services.enrollment_service import EnrollmentService
from app.api.auth import get_current_active_user, get_current_admin_user

router = APIRouter()

@router.get("/", response_model=List[CourseResponse])
async def list_courses(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(database.get_db)
):
    course_service = CourseService(db)
    return await course_service.get_multi(skip=skip, limit=limit)

@router.post("/", response_model=CourseResponse)
async def create_course(
    course: CourseCreate,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(database.get_db)
):
    course_service = CourseService(db)
    return await course_service.create(course=course, owner_id=current_user.id)

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(
    course_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(database.get_db)
):
    course_service = CourseService(db)
    course = await course_service.get(id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.get("/{course_id}/lessons", response_model=List[LessonResponse])
async def get_course_lessons(
    course_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(database.get_db)
):
    lesson_service = LessonService(db)
    return await lesson_service.get_by_course(course_id=course_id, skip=skip, limit=limit)

@router.post("/{course_id}/purchase", response_model=EnrollmentResponse)
async def purchase_course(
    course_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(database.get_db)
):
    enrollment_service = EnrollmentService(db)
    course_service = CourseService(db)

    # Проверяем, существует ли курс
    course = await course_service.get(id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Проверяем, не записан ли пользователь уже на курс
    existing_enrollment = await enrollment_service.get_by_user_and_course(
        user_id=current_user.id, course_id=course_id
    )
    if existing_enrollment:
        raise HTTPException(status_code=400, detail="Already enrolled in this course")

    # Создаем запись с доступом на 30 дней
    enrollment_data = EnrollmentCreate(
        course_id=course_id,
        expires_at=datetime.utcnow() + timedelta(days=30)
    )

    return await enrollment_service.create(enrollment_data, user_id=current_user.id)
