from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

from app.core.database import get_postgres_session, get_mongo_db
from app.models.pydantic_schemas import ProgressUpdate, ProgressResponse
from app.core.security import get_current_user
from app.models.sql_models import User
from app.services.progress_service import ProgressService

router = APIRouter()

@router.post("/{lesson_id}", response_model=ProgressResponse)
async def update_progress(
    lesson_id: int, 
    progress_in: ProgressUpdate, 
    current_user: User = Depends(get_current_user),
    pg_db: AsyncSession = Depends(get_postgres_session),
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    service = ProgressService(pg_db, mongo_db)
    return await service.update_lesson_progress(lesson_id, progress_in, current_user)

@router.get("/{course_id}", response_model=List[ProgressResponse])
async def get_course_progress(
    course_id: int, 
    current_user: User = Depends(get_current_user),
    pg_db: AsyncSession = Depends(get_postgres_session),
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    service = ProgressService(pg_db, mongo_db)
    return await service.get_course_progress(course_id, current_user)
