from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_postgres_session
from app.models.sql_models import User
from app.models.pydantic_schemas import CourseCreate, CourseResponse
from app.core.security import get_current_user
from app.services.course_service import CourseService

router = APIRouter()

@router.get("/", response_model=List[CourseResponse])
async def get_courses(db: AsyncSession = Depends(get_postgres_session)):
    service = CourseService(db)
    return await service.get_all_courses()

@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_in: CourseCreate, 
    db: AsyncSession = Depends(get_postgres_session),
    current_user: User = Depends(get_current_user)
):
    service = CourseService(db)
    return await service.create_course(course_in, current_user)

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(course_id: int, db: AsyncSession = Depends(get_postgres_session)):
    service = CourseService(db)
    return await service.get_course(course_id)
