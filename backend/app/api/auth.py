from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_postgres_session
from app.models.sql_models import User
from app.models.pydantic_schemas import UserCreate, Token, UserResponse
from app.core.security import get_password_hash, verify_password, create_access_token, get_current_user
from app.repositories.user_repository import UserRepository
from app.services.email_service import EmailService

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_postgres_session)):
    repo = UserRepository(db)
    existing_user = await repo.get_by_email(user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = User(email=user_in.email, hashed_password=get_password_hash(user_in.password))
    user = await repo.create(user)
    
    # Отправка приветственного письма через Redis Queue
    await EmailService.queue_welcome_email(user.id, user.email)
    
    return user

@router.post("/login", response_model=Token)
async def login(user_in: UserCreate, db: AsyncSession = Depends(get_postgres_session)):
    repo = UserRepository(db)
    user = await repo.get_by_email(user_in.email)
    
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
