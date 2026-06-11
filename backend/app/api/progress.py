from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from motor.motor_asyncio import AsyncIOMotorClient

from app.core import database
from app.models.sql_models import User, Lesson, Progress, Enrollment
from app.models.pydantic_schemas import (
    ProgressCreate, ProgressUpdate, ProgressResponse,
    CourseResponse
)
from app.services.progress_service import ProgressService
from app.api.auth import get_current_active_user

router = APIRouter()

@router.post("/progress/{lesson_id}", response_model=ProgressResponse)
async def update_progress(
    lesson_id: int,
    progress_data: ProgressUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(database.get_db),
    mongo_client: AsyncIOMotorClient = Depends(database.mongo_client)
):
    # Проверяем, что пользователь имеет доступ к уроку
    enrollment = await database.db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id,
        Enrollment.expires_at > datetime.utcnow()
    ).join(Course).join(Lesson).filter(
        Lesson.id == lesson_id
    ).first()

    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this lesson"
        )

    # Обновляем прогресс в MongoDB
    progress_service = ProgressService(mongo_client)
    progress = await progress_service.update_progress(
        user_id=current_user.id,
        lesson_id=lesson_id,
        watched_seconds=progress_data.watched_seconds,
        is_completed=progress_data.is_completed
    )

    return progress

@router.get("/progress/{course_id}", response_model=List[ProgressResponse])
async def get_course_progress(
    course_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(database.get_db),
    mongo_client: AsyncIOMotorClient = Depends(database.mongo_client)
):
    # Проверяем, что пользователь имеет доступ к курсу
    enrollment = await database.db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id,
        Enrollment.course_id == course_id,
        Enrollment.expires_at > datetime.utcnow()
    ).first()

    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this course"
        )

    # Получаем прогресс по курсу из MongoDB
    progress_service = ProgressService(mongo_client)
    return await progress_service.get_progress_by_course(
        user_id=current_user.id,
        course_id=course_id
    )
