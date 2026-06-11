from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.core import database
from app.models.sql_models import User, Course, Lesson
from app.models.pydantic_schemas import (
    CourseCreate, CourseUpdate, CourseResponse,
    LessonCreate, LessonUpdate, LessonResponse,
    VideoConversionSchema
)
from app.services.course_service import CourseService
from app.services.lesson_service import LessonService
from app.api.auth import get_current_admin_user
from app.workers.rabbitmq_consumer import send_to_video_conversion

router = APIRouter()

@router.post("/courses", response_model=CourseResponse)
async def create_course(
    course: CourseCreate,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(database.get_db)
):
    course_service = CourseService(db)
    return await course_service.create(course=course, owner_id=current_user.id)

@router.put("/courses/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: int,
    course: CourseUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(database.get_db)
):
    course_service = CourseService(db)
    course_obj = await course_service.get(id=course_id)

    if not course_obj:
        raise HTTPException(status_code=404, detail="Course not found")

    if course_obj.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return await course_service.update(id=course_id, obj_in=course)

@router.delete("/courses/{course_id}")
async def delete_course(
    course_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(database.get_db)
):
    course_service = CourseService(db)
    course_obj = await course_service.get(id=course_id)

    if not course_obj:
        raise HTTPException(status_code=404, detail="Course not found")

    if course_obj.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    await course_service.delete(id=course_id)
    return {"detail": "Course deleted successfully"}

@router.post("/lessons", response_model=LessonResponse)
async def create_lesson(
    lesson: LessonCreate,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(database.get_db)
):
    # Проверяем, что курс существует и пользователь имеет права
    course_service = CourseService(db)
    course_obj = await course_service.get(id=lesson.course_id)

    if not course_obj:
        raise HTTPException(status_code=404, detail="Course not found")

    if course_obj.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    lesson_service = LessonService(db)
    return await lesson_service.create(lesson=lesson)

@router.put("/lessons/{lesson_id}", response_model=LessonResponse)
async def update_lesson(
    lesson_id: int,
    lesson: LessonUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(database.get_db)
):
    lesson_service = LessonService(db)
    lesson_obj = await lesson_service.get(id=lesson_id)

    if not lesson_obj:
        raise HTTPException(status_code=404, detail="Lesson not found")

    # Проверяем, что пользователь имеет права
    course_service = CourseService(db)
    course_obj = await course_service.get(id=lesson_obj.course_id)

    if course_obj.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return await lesson_service.update(id=lesson_id, obj_in=lesson)

@router.delete("/lessons/{lesson_id}")
async def delete_lesson(
    lesson_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(database.get_db)
):
    lesson_service = LessonService(db)
    lesson_obj = await lesson_service.get(id=lesson_id)

    if not lesson_obj:
        raise HTTPException(status_code=404, detail="Lesson not found")

    # Проверяем, что пользователь имеет права
    course_service = CourseService(db)
    course_obj = await course_service.get(id=lesson_obj.course_id)

    if course_obj.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    await lesson_service.delete(id=lesson_id)
    return {"detail": "Lesson deleted successfully"}

@router.post("/upload-video")
async def upload_video(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(database.get_db)
):
    # Проверяем, что пользователь является администратором
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # Здесь должна быть логика загрузки файла в S3 или другую систему хранения
    # Для примера просто симулируем процесс
    video_id = f"video_{datetime.now().timestamp()}"
    video_path = f"/tmp/{video_id}"

    # Отправляем задачу на конвертацию видео в RabbitMQ
    video_data = VideoConversionSchema(
        video_id=video_id,
        video_path=video_path,
        output_format="mp4"
    )

    await send_to_video_conversion(video_data)

    return {
        "detail": "Video uploaded successfully",
        "video_id": video_id,
        "message": "Video conversion task has been queued"
    }
