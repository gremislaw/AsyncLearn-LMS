import asyncio
import json
from aio_pika import connect_robust, Message, IncomingMessage
from app.core.config import settings

# Переменная для хранения соединения
rabbitmq_connection = None
rabbitmq_channel = None

async def get_rabbitmq_connection():
    global rabbitmq_connection, rabbitmq_channel
    if rabbitmq_connection is None:
        rabbitmq_connection = await connect_robust(
            host=settings.RABBITMQ_SERVER,
            port=settings.RABBITMQ_PORT,
            login=settings.RABBITMQ_USER,
            password=settings.RABBITMQ_PASSWORD
        )
        rabbitmq_channel = await rabbitmq_connection.channel()
        # Объявляем очередь
        await rabbitmq_channel.declare_queue(settings.RABBITMQ_QUEUE_VIDEO, durable=True)
    return rabbitmq_connection, rabbitmq_channel

async def send_to_video_conversion(video_data: dict):
    connection, channel = await get_rabbitmq_connection()
    message = Message(
        body=json.dumps(video_data).encode(),
        delivery_mode=2,  # Делаем сообщение постоянным
    )
    await channel.default_exchange.publish(
        message,
        routing_key=settings.RABBITMQ_QUEUE_VIDEO,
    )
    print(f"Sent video conversion task: {video_data}")

async def process_video_conversion(message: IncomingMessage):
    async with message.process():
        try:
            video_data = json.loads(message.body.decode())
            print(f"Received video conversion task: {video_data}")
            # Здесь будет логика конвертации видео
            # Для примера просто симулируем обработку
            await asyncio.sleep(2)
            print(f"Video conversion completed: {video_data.get('video_id')}")
        except Exception as e:
            print(f"Error processing video conversion: {e}")

async def start_video_consumer():
    connection, channel = await get_rabbitmq_connection()
    queue = await channel.declare_queue(settings.RABBITMQ_QUEUE_VIDEO, durable=True)
    await queue.consume(process_video_conversion)
    print("RabbitMQ consumer started")
    try:
        await asyncio.Future()  # Ожидаем завершения
    finally:
        await connection.close()

async def stop_rabbitmq():
    global rabbitmq_connection
    if rabbitmq_connection:
        await rabbitmq_connection.close()
        rabbitmq_connection = None
        rabbitmq_channel = None
