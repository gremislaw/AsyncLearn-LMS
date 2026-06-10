import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from unittest.mock import AsyncMock, MagicMock

from app.main import app
from app.core.database import get_postgres_session, get_mongo_db, get_redis
from app.core.config import settings
from app.models.sql_models import Base, User
from app.core.security import get_password_hash, create_access_token

TEST_DATABASE_URL = "postgresql+asyncpg://admin:admin@localhost:5432/asynclms_test"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def override_get_postgres_session():
    async with TestSessionLocal() as session:
        yield session

mock_mongo = AsyncMock()
mock_mongo.progress = AsyncMock()
mock_mongo.progress.update_one = AsyncMock()
mock_mongo.progress.find = MagicMock(return_value=AsyncMock())

mock_redis = AsyncMock()
mock_redis.brpop = AsyncMock(return_value=None)
mock_redis.rpush = AsyncMock()

app.dependency_overrides[get_postgres_session] = override_get_postgres_session
app.dependency_overrides[get_mongo_db] = lambda: mock_mongo
app.dependency_overrides[get_redis] = lambda: mock_redis

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def admin_token():
    async with TestSessionLocal() as session:
        user = User(email="admin@test.com", hashed_password=get_password_hash("password"), role="admin")
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return create_access_token(data={"sub": user.id})

@pytest.fixture
async def student_token():
    async with TestSessionLocal() as session:
        user = User(email="student@test.com", hashed_password=get_password_hash("password"), role="student")
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return create_access_token(data={"sub": user.id})
