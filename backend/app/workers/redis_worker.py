import asyncio
from redis.asyncio import Redis
from app.core.config import settings
from app.core.database import AsyncSession
from app.services.email_service import EmailService

class RedisWorker:
    def __init__(self):
        self.redis_client = Redis(
            host=settings.REDIS_SERVER,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )
        self.email_service = EmailService()
        self.is_running = False

    async def start_worker(self):
        self.is_running = True
        asyncio.create_task(self.process_queue())

    async def stop_worker(self):
        self.is_running = False
        await self.redis_client.close()

    async def process_queue(self):
        while self.is_running:
            try:
                # Получаем задачу из очереди
                task = await self.redis_client.brpop("email_queue", timeout=1)
                if not task:
                    continue

                _, task_data = task
                email_data = eval(task_data)  # В реальном проекте лучше использовать JSON

                # Обработка задачи
                await self.email_service.send_welcome_email(
                    to=email_data["to"],
                    username=email_data["username"]
                )

                print(f"Processed email task: {email_data}")

            except Exception as e:
                print(f"Error processing Redis queue: {e}")
                await asyncio.sleep(1)

# Создаем экземпляр воркера
redis_worker = RedisWorker()

# Функции для запуска и остановки воркера
async def start_worker():
    await redis_worker.start_worker()

async def stop_worker():
    await redis_worker.stop_worker()
