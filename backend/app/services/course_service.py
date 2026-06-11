from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.models.sql_models import Course
from app.models.pydantic_schemas import CourseCreate, CourseUpdate

class CourseService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, course: CourseCreate, owner_id: int) -> Course:
        db_course = Course(
            title=course.title,
            description=course.description,
            price=course.price,
            is_active=course.is_active,
            owner_id=owner_id
        )
        self.db.add(db_course)
        await self.db.commit()
        await self.db.refresh(db_course)
        return db_course

    async def get(self, id: int) -> Optional[Course]:
        query = select(Course).where(Course.id == id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_multi(self, skip: int = 0, limit: int = 100) -> List[Course]:
        query = select(Course).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update(self, id: int, obj_in: CourseUpdate) -> Optional[Course]:
        course = await self.get(id)
        if not course:
            return None

        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(course, field, value)

        await self.db.commit()
        await self.db.refresh(course)
        return course

    async def delete(self, id: int) -> bool:
        course = await self.get(id)
        if not course:
            return False

        await self.db.delete(course)
        await self.db.commit()
        return True
