import asyncio
from app.core.kafka import kafka_consumer
from app.services.email_service import EmailService

class KafkaConsumer:
    def __init__(self):
        self.is_running = False

    async def start_consumer(self):
        self.is_running = True
        asyncio.create_task(self.process_messages())

    async def stop_consumer(self):
        self.is_running = False

    async def process_messages(self):
        while self.is_running:
            try:
                # Получаем сообщения из Kafka
                async for message in kafka_consumer:
                    # Обрабатываем сообщение
                    data = message.value
                    print(f"Received Kafka message: {data}")

                    # Отправляем email уведомление о покупке
                    email_service = EmailService()
                    await email_service.send_purchase_confirmation(
                        to=data["email"],
                        course_name=data["course_name"],
                        amount=data["amount"]
                    )

            except Exception as e:
                print(f"Error processing Kafka message: {e}")
                await asyncio.sleep(1)

# Создаем экземпляр консьюмера
kafka_consumer_instance = KafkaConsumer()

# Функции для запуска и остановки консьюмера
async def start_consumer():
    await kafka_consumer_instance.start_consumer()

async def stop_consumer():
    await kafka_consumer_instance.stop_consumer()
