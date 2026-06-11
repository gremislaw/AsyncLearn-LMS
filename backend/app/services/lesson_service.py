from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.models.sql_models import Lesson
from app.models.pydantic_schemas import LessonCreate, LessonUpdate

class LessonService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, lesson: LessonCreate) -> Lesson:
        db_lesson = Lesson(
            title=lesson.title,
            description=lesson.description,
            video_url=lesson.video_url,
            duration=lesson.duration,
            order=lesson.order,
            is_active=lesson.is_active,
            course_id=lesson.course_id
        )
        self.db.add(db_lesson)
        await self.db.commit()
        await self.db.refresh(db_lesson)
        return db_lesson

    async def get(self, id: int) -> Optional[Lesson]:
        query = select(Lesson).where(Lesson.id == id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_course(self, course_id: int, skip: int = 0, limit: int = 100) -> List[Lesson]:
        query = select(Lesson).where(Lesson.course_id == course_id).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update(self, id: int, obj_in: LessonUpdate) -> Optional[Lesson]:
        lesson = await self.get(id)
        if not lesson:
            return None

        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(lesson, field, value)

        await self.db.commit()
        await self.db.refresh(lesson)
        return lesson

    async def delete(self, id: int) -> bool:
        lesson = await self.get(id)
        if not lesson:
            return False

        await self.db.delete(lesson)
        await self.db.commit()
        return True
