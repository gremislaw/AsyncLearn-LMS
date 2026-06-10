import asyncio
import json
import logging
from aiokafka import AIOKafkaConsumer
from app.core.config import settings

logger = logging.getLogger(__name__)

async def consume_purchase_events() -> None:
    consumer = AIOKafkaConsumer(
        settings.KAFKA_TOPIC_PURCHASE,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id="lms_email_service",
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )
    await consumer.start()
    logger.info("Kafka Consumer: Started listening for purchase events...")
    try:
        async for msg in consumer:
            data = msg.value
            email = data.get("email")
            logger.info(f"Sending purchase confirmation email to {email}")
            await asyncio.sleep(1)
    except Exception as e:
        logger.error(f"Kafka Consumer error: {e}")
    finally:
        await consumer.stop()
