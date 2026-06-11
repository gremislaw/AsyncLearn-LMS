from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis
from .config import settings

# PostgreSQL
DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

engine = create_async_engine(
    DATABASE_URL,
    poolclass=NullPool,
    echo=settings.DEBUG
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

BaseSQL = declarative_base()

# MongoDB
MONGO_URL = f"mongodb://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@{settings.MONGO_SERVER}:{settings.MONGO_PORT}/{settings.MONGO_DB}"

mongo_client = AsyncIOMotorClient(MONGO_URL)
mongo_db = mongo_client[settings.MONGO_DB]

# Redis
redis_client = Redis(
    host=settings.REDIS_SERVER,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)

# Функции для получения сессий
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

# Функция для инициализации БД
async def init_db():
    # Создание таблиц PostgreSQL
    async with engine.begin() as conn:
        await conn.run_sync(BaseSQL.metadata.create_all)
