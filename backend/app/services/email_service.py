import json
import logging
from app.core.database import get_redis

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    async def queue_welcome_email(user_id: int, email: str) -> None:
        redis = get_redis()
        payload = json.dumps({"user_id": user_id, "email": email})
        await redis.rpush("email_welcome_queue", payload)
        logger.info(f"Queued welcome email for {email}")
