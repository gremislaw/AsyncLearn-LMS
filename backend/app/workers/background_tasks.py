import asyncio
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.models.sql_models import Enrollment, User
from app.services.email_service import EmailService
from app.core.config import settings

class BackgroundTasks:
    def __init__(self):
        self.is_running = False

    async def start_background_tasks(self):
        self.is_running = True
        asyncio.create_task(self.check_expired_enrollments())

    async def stop_background_tasks(self):
        self.is_running = False

    async def check_expired_enrollments(self):
        while self.is_running:
            try:
                # Получаем все истекающие записи
                async with AsyncSessionLocal() as db:
                    expired_enrollments = await db.query(Enrollment).filter(
                        Enrollment.expires_at <= datetime.utcnow()
                    ).all()

                    # Отправляем уведомления об истечении доступа
                    email_service = EmailService()

                    for enrollment in expired_enrollments:
                        # Получаем пользователя
                        user = await db.query(User).filter(User.id == enrollment.user_id).first()

                        if user:
                            await email_service.send_access_expiry_notification(
                                to=user.email,
                                course_name=f"Course ID: {enrollment.course_id}",
                                expiry_date=enrollment.expires_at.strftime("%Y-%m-%d")
                            )

                            # Обновляем запись, чтобы не отправлять уведомления повторно
                            enrollment.expires_at = datetime.utcnow() - timedelta(days=1)
                            await db.commit()

                    print(f"Processed {len(expired_enrollments)} expired enrollments")

            except Exception as e:
                print(f"Error checking expired enrollments: {e}")

            # Проверяем раз в день
            await asyncio.sleep(24 * 60 * 60)

# Создаем экземпляр фоновых задач
background_tasks = BackgroundTasks()

# Функции для запуска и остановки фоновых задач
async def start_background_tasks():
    await background_tasks.start_background_tasks()

async def stop_background_tasks():
    await background_tasks.stop_background_tasks()
