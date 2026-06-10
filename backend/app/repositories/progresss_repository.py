from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Dict, Any

class ProgressRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.progress

    async def update_progress(self, user_id: int, lesson_id: int, watched_seconds: int, is_completed: bool) -> Dict[str, Any]:
        progress_data = {
            "user_id": user_id,
            "lesson_id": lesson_id,
            "watched_seconds": watched_seconds,
            "is_completed": is_completed
        }
        await self.collection.update_one(
            {"user_id": user_id, "lesson_id": lesson_id},
            {"$set": progress_data},
            upsert=True
        )
        return progress_data

    async def get_course_progress(self, user_id: int, lesson_ids: List[int]) -> List[Dict[str, Any]]:
        cursor = self.collection.find(
            {"user_id": user_id, "lesson_id": {"$in": lesson_ids}}
        )
        return await cursor.to_list(length=100)
