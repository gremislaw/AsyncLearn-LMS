from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.kafka import kafka_producer
from app.models.sql_models import Purchase, Course, User
from app.repositories.course_repository import CourseRepository
from fastapi import HTTPException

class PaymentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.course_repo = CourseRepository(db)

    async def purchase_course(self, course_id: int, current_user: User) -> Purchase:
        course = await self.course_repo.get_by_id(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        # Mock платежа
        purchase = Purchase(
            user_id=current_user.id,
            course_id=course_id,
            expiry_date=datetime.utcnow() + timedelta(days=30),
            is_active=True
        )
        self.db.add(purchase)
        await self.db.commit()
        await self.db.refresh(purchase)

        # Отправка события в Kafka
        await kafka_producer.send_purchase_event(
            user_id=current_user.id,
            course_id=course_id,
            email=current_user.email
        )

        return purchase
