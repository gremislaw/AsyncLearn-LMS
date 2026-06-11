from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from app.core.config import settings
import asyncio
import json

# Создаем продюсера
kafka_producer = AIOKafkaProducer(
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode()
)

# Создаем консьюмера
kafka_consumer = AIOKafkaConsumer(
    settings.KAFKA_TOPIC_EMAILS,
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    group_id="email_service",
    value_deserializer=lambda m: json.loads(m.decode())
)

async def start_kafka_producer():
    await kafka_producer.start()

async def stop_kafka_producer():
    await kafka_producer.stop()

async def send_email_notification(data: dict):
    await kafka_producer.send_and_wait(settings.KAFKA_TOPIC_EMAILS, value=data)

async def start_kafka_consumer():
    await kafka_consumer.start()
    async for message in kafka_consumer:
        # Обработка сообщений
        try:
            data = message.value
            print(f"Received email notification: {data}")
            # Здесь будет логика отправки email
        except Exception as e:
            print(f"Error processing Kafka message: {e}")

# Функция для запуска консьюмера в отдельном потоке
async def run_kafka_consumer():
    asyncio.create_task(start_kafka_consumer())
