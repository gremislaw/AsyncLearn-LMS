from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.course_repository import CourseRepository
from app.models.sql_models import Course, User
from app.models.pydantic_schemas import CourseCreate

class CourseService:
    def __init__(self, db: AsyncSession):
        self.repo = CourseRepository(db)

    async def get_all_courses(self) -> list[Course]:
        return await self.repo.get_all()

    async def get_course(self, course_id: int) -> Course:
        course = await self.repo.get_by_id(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        return course

    async def create_course(self, course_in: CourseCreate, current_user: User) -> Course:
        if current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Only admins can create courses")
        
        course = Course(**course_in.model_dump(), owner_id=current_user.id)
        return await self.repo.create(course)
