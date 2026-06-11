from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from typing import Optional
from app.models.sql_models import Enrollment, Course, User
from app.models.pydantic_schemas import PaymentCreate
import uuid

class PaymentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_payment(self, payment: PaymentCreate, user_id: int) -> dict:
        # Генерируем ID платежа
        payment_id = str(uuid.uuid4())

        # Получаем курс
        course_query = select(Course).where(Course.id == payment.course_id)
        course_result = await self.db.execute(course_query)
        course = course_result.scalar_one_or_none()

        if not course:
            raise ValueError("Course not found")

        # Проверяем, не записан ли пользователь уже на курс
        enrollment_query = select(Enrollment).where(
            Enrollment.user_id == user_id,
            Enrollment.course_id == payment.course_id
        )
        enrollment_result = await self.db.execute(enrollment_query)
        existing_enrollment = enrollment_result.scalar_one_or_none()

        if existing_enrollment:
            return {
                "payment_id": payment_id,
                "status": "already_enrolled",
                "message": "User is already enrolled in this course"
            }

        # Создаем запись о платеже
        payment_record = {
            "payment_id": payment_id,
            "user_id": user_id,
            "course_id": payment.course_id,
            "amount": course.price,
            "status": "pending",
            "created_at": datetime.utcnow(),
            "payment_method": payment.payment_method
        }

        # В реальном приложении здесь была бы интеграция с платежной системой
        # Для примера симулируем успешную оплату
        payment_record["status"] = "completed"

        # Создаем запись об enrollment
        enrollment = Enrollment(
            user_id=user_id,
            course_id=payment.course_id,
            enrolled_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=30)
        )

        self.db.add(enrollment)
        await self.db.commit()

        # Отправляем событие в Kafka о покупке
        from app.core.kafka import send_email_notification
        await send_email_notification({
            "email": user.email,  # Нужно получить email пользователя
            "course_name": course.title,
            "amount": course.price
        })

        return {
            "payment_id": payment_id,
            "status": "completed",
            "enrollment_id": enrollment.id
        }

    async def get_payment_status(self, payment_id: str) -> Optional[dict]:
        # В реальном приложении здесь был бы запрос к платежной системе
        # Для примера возвращаем статический ответ
        return {
            "payment_id": payment_id,
            "status": "completed"
        }
