import asyncio
import json
import logging
import aio_pika
from app.core.config import settings

logger = logging.getLogger(__name__)

async def process_video_conversion() -> None:
    try:
        connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        channel = await connection.channel()
        queue = await channel.declare_queue("video_conversion", durable=True)

        async with queue.iterator() as queue_iter:
            logger.info("RabbitMQ Consumer: Started listening for video conversions...")
            async for message in queue_iter:
                async with message.process():
                    data = json.loads(message.body.decode())
                    video_path = data.get("video_path")
                    logger.info(f"Starting video conversion for {video_path}")
                    await asyncio.sleep(3) 
                    logger.info(f"Video conversion completed for {video_path}")
    except Exception as e:
        logger.error(f"RabbitMQ Consumer error: {e}")
