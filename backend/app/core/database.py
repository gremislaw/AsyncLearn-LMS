from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis
from app.core.config import settings

# PostgreSQL
engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# MongoDB
mongo_client = AsyncIOMotorClient(settings.MONGO_URL)
mongo_db = mongo_client[settings.MONGO_DB]

# Redis
redis_client = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)

async def get_postgres_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

def get_mongo_db():
    return mongo_db

def get_redis() -> Redis:
    return redis_client
