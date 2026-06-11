import asyncio
from app.core.rabbitmq import start_video_consumer, stop_rabbitmq
from app.core.config import settings
from app.services.video_service import VideoService

class RabbitMQConsumer:
    def __init__(self):
        self.is_running = False

    async def start_consumer(self):
        self.is_running = True
        asyncio.create_task(start_video_consumer())

    async def stop_consumer(self):
        self.is_running = False
        await stop_rabbitmq()

# Создаем экземпляр консьюмера
rabbitmq_consumer_instance = RabbitMQConsumer()

# Функции для запуска и остановки консьюмера
async def start_consumer():
    await rabbitmq_consumer_instance.start_consumer()

async def stop_consumer():
    await rabbitmq_consumer_instance.stop_consumer()
