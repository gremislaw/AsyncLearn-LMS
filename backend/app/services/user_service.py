from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.sql_models import User
from app.models.pydantic_schemas import UserCreate
from app.core import security

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_username(self, username: str) -> User | None:
        query = select(User).where(User.username == username)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, user: UserCreate) -> User:
        hashed_password = security.get_password_hash(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            role=user.role
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def authenticate(self, username: str, password: str) -> User | None:
        user = await self.get_by_username(username)
        if not user:
            return None
        if not security.verify_password(password, user.hashed_password):
            return None
        return user

    async def get(self, id: int) -> User | None:
        query = select(User).where(User.id == id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def update(self, id: int, obj_in) -> User:
        user = await self.get(id)
        if not user:
            return None

        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(user, field, value)

        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete(self, id: int) -> bool:
        user = await self.get(id)
        if not user:
            return False

        await self.db.delete(user)
        await self.db.commit()
        return True
