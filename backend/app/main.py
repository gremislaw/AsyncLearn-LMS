from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, courses, progress, admin
from app.core import config, database
from app.workers import redis_worker, kafka_consumer, rabbitmq_consumer, background_tasks
import uvicorn

app = FastAPI(
    title="AsyncLearn LMS",
    description="Асинхронная платформа онлайн-обучения",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене нужно указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(auth.router, prefix="/auth", tags=["Аутентификация"])
app.include_router(courses.router, prefix="/courses", tags=["Курсы"])
app.include_router(progress.router, prefix="/progress", tags=["Прогресс"])
app.include_router(admin.router, prefix="/admin", tags=["Администрирование"])

# Healthcheck эндпоинт
@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.on_event("startup")
async def startup_event():
    # Запуск воркеров
    await redis_worker.start_worker()
    await kafka_consumer.start_consumer()
    await rabbitmq_consumer.start_consumer()
    await background_tasks.start_background_tasks()

@app.on_event("shutdown")
async def shutdown_event():
    # Остановка воркеров
    await redis_worker.stop_worker()
    await kafka_consumer.stop_consumer()
    await rabbitmq_consumer.stop_consumer()
    await background_tasks.stop_background_tasks()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
