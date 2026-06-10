import asyncio
import logging
from datetime import datetime
from sqlalchemy import select, and_
from app.core.database import AsyncSessionLocal
from app.models.sql_models import Purchase

logger = logging.getLogger(__name__)

async def check_expired_access() -> None:
    while True:
        await asyncio.sleep(60)
        try:
            async with AsyncSessionLocal() as session:
                now = datetime.utcnow()
                result = await session.execute(
                    select(Purchase).where(and_(Purchase.is_active == True, Purchase.expiry_date <= now))
                )
                expired_purchases = result.scalars().all()
                for purchase in expired_purchases:
                    purchase.is_active = False
                    logger.info(f"Access expired for User {purchase.user_id}, Course {purchase.course_id}")
                await session.commit()
        except Exception as e:
            logger.error(f"Background task error: {e}")
