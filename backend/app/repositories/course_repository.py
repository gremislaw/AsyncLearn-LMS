from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.models.sql_models import Course

class CourseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> List[Course]:
        result = await self.db.execute(select(Course))
        return result.scalars().all()

    async def get_by_id(self, course_id: int) -> Optional[Course]:
        return await self.db.get(Course, course_id)

    async def create(self, course: Course) -> Course:
        self.db.add(course)
        await self.db.commit()
        await self.db.refresh(course)
        return course
