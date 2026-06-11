from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional, Dict, Any
from datetime import datetime

class ProgressService:
    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.db = mongo_client["asynclearn"]
        self.collection = self.db["progress"]

    async def update_progress(self, user_id: int, lesson_id: int, watched_seconds: int, is_completed: bool) -> Dict[str, Any]:
        # Обновляем или создаем запись прогресса
        progress_data = {
            "user_id": user_id,
            "lesson_id": lesson_id,
            "watched_seconds": watched_seconds,
            "is_completed": is_completed,
            "last_watched_at": datetime.utcnow()
        }

        result = await self.collection.update_one(
            {"user_id": user_id, "lesson_id": lesson_id},
            {"$set": progress_data},
            upsert=True
        )

        return progress_data

    async def get_progress_by_course(self, user_id: int, course_id: int) -> List[Dict[str, Any]]:
        # Получаем все уроки курса
        lessons = await self.db["lessons"].find({"course_id": course_id}).to_list(None)
        lesson_ids = [lesson["id"] for lesson in lessons]

        # Получаем прогресс пользователя по этим урокам
        progress = await self.collection.find({
            "user_id": user_id,
            "lesson_id": {"$in": lesson_ids}
        }).to_list(None)

        return progress

    async def get_progress_by_lesson(self, user_id: int, lesson_id: int) -> Optional[Dict[str, Any]]:
        progress = await self.collection.find_one({
            "user_id": user_id,
            "lesson_id": lesson_id
        })
        return progress

    async def get_course_completion_percentage(self, user_id: int, course_id: int) -> float:
        # Получаем все уроки курса
        lessons = await self.db["lessons"].find({"course_id": course_id}).to_list(None)
        total_lessons = len(lessons)

        if total_lessons == 0:
            return 0.0

        # Получаем количество пройденных уроков
        completed_lessons = await self.collection.count_documents({
            "user_id": user_id,
            "lesson_id": {"$in": [lesson["id"] for lesson in lessons]},
            "is_completed": True
        })

        return (completed_lessons / total_lessons) * 100
