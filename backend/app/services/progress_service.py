from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.repositories.progress_repository import ProgressRepository
from app.models.sql_models import Lesson, User
from app.models.pydantic_schemas import ProgressUpdate, ProgressResponse
from typing import List

class ProgressService:
    def __init__(self, pg_db: AsyncSession, mongo_db: AsyncIOMotorDatabase):
        self.pg_db = pg_db
        self.progress_repo = ProgressRepository(mongo_db)

    async def update_lesson_progress(self, lesson_id: int, progress_in: ProgressUpdate, current_user: User) -> dict:
        lesson = await self.pg_db.get(Lesson, lesson_id)
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")

        return await self.progress_repo.update_progress(
            user_id=current_user.id,
            lesson_id=lesson_id,
            watched_seconds=progress_in.watched_seconds,
            is_completed=progress_in.is_completed
        )

    async def get_course_progress(self, course_id: int, current_user: User) -> List[dict]:
        result = await self.pg_db.execute(select(Lesson).where(Lesson.course_id == course_id))
        lessons = result.scalars().all()
        lesson_ids = [lesson.id for lesson in lessons]

        return await self.progress_repo.get_course_progress(
            user_id=current_user.id,
            lesson_ids=lesson_ids
        )
