from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging

from app.core.config import settings
from app.core.database import engine
from app.models.sql_models import Base
from app.api import auth, courses, progress, admin
from app.core.kafka import kafka_producer
from app.core.rabbitmq import rabbitmq_client
from app.workers.redis_worker import process_welcome_email_queue
from app.workers.kafka_consumer import consume_purchase_events
from app.workers.rabbitmq_consumer import process_video_conversion
from app.workers.background_tasks import check_expired_access

logging.basicConfig(level=logging.INFO)

background_tasks_list = []

async def start_background_tasks():
    task1 = asyncio.create_task(process_welcome_email_queue())
    task2 = asyncio.create_task(consume_purchase_events())
    task3 = asyncio.create_task(process_video_conversion())
    task4 = asyncio.create_task(check_expired_access())
    background_tasks_list.extend([task1, task2, task3, task4])

async def stop_background_tasks():
    for task in background_tasks_list:
        task.cancel()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await kafka_producer.start()
    await rabbitmq_client.connect()
    await start_background_tasks()
    yield
    await kafka_producer.stop()
    await rabbitmq_client.close()
    await stop_background_tasks()

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Auth"])
app.include_router(courses.router, prefix=f"{settings.API_V1_STR}/courses", tags=["Courses"])
app.include_router(progress.router, prefix=f"{settings.API_V1_STR}/progress", tags=["Progress"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["Admin"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": settings.PROJECT_NAME}
