from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from typing import Optional, List
from app.models.sql_models import Enrollment, Course, User
from app.models.pydantic_schemas import EnrollmentCreate

class EnrollmentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, enrollment: EnrollmentCreate, user_id: int) -> Enrollment:
        db_enrollment = Enrollment(
            user_id=user_id,
            course_id=enrollment.course_id,
            enrolled_at=datetime.utcnow(),
            expires_at=enrollment.expires_at
        )
        self.db.add(db_enrollment)
        await self.db.commit()
        await self.db.refresh(db_enrollment)
        return db_enrollment

    async def get(self, id: int) -> Optional[Enrollment]:
        query = select(Enrollment).where(Enrollment.id == id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_user_and_course(self, user_id: int, course_id: int) -> Optional[Enrollment]:
        query = select(Enrollment).where(
            Enrollment.user_id == user_id,
            Enrollment.course_id == course_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_user_enrollments(self, user_id: int) -> List[Enrollment]:
        query = select(Enrollment).where(Enrollment.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_course_enrollments(self, course_id: int) -> List[Enrollment]:
        query = select(Enrollment).where(Enrollment.course_id == course_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def is_enrolled(self, user_id: int, course_id: int) -> bool:
        enrollment = await self.get_by_user_and_course(user_id, course_id)
        return enrollment is not None

    async def has_active_access(self, user_id: int, course_id: int) -> bool:
        enrollment = await self.get_by_user_and_course(user_id, course_id)
        if not enrollment:
            return False

        return enrollment.expires_at > datetime.utcnow()

    async def extend_access(self, enrollment_id: int, days: int = 30) -> Optional[Enrollment]:
        enrollment = await self.get(enrollment_id)
        if not enrollment:
            return None

        enrollment.expires_at += timedelta(days=days)
        await self.db.commit()
        await self.db.refresh(enrollment)
        return enrollment

    async def delete(self, id: int) -> bool:
        enrollment = await self.get(id)
        if not enrollment:
            return False

        await self.db.delete(enrollment)
        await self.db.commit()
        return True
