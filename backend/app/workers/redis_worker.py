import asyncio
import json
import logging
from app.core.database import get_redis

logger = logging.getLogger(__name__)

async def process_welcome_email_queue() -> None:
    redis = get_redis()
    logger.info("Redis Worker: Started listening for welcome emails...")
    
    while True:
        try:
            message = await redis.brpop("email_welcome_queue", timeout=5)
            if message:
                _, payload = message
                data = json.loads(payload)
                email = data.get("email")
                logger.info(f"Sending welcome email to {email}")
                await asyncio.sleep(1)
                logger.info(f"Welcome email sent to {email}")
        except Exception as e:
            logger.error(f"Redis Worker error: {e}")
            await asyncio.sleep(5)
