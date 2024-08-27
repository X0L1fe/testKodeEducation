from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import UserCreate, UserSchema
from app.database import AsyncSessionLocal
from app.crud import get_user_by_username, create_user, authenticate_user
from app.utils import create_access_token, SECRET_KEY as secret, ALGORITHM as alg

SECRET_KEY = secret
ALGORITHM = alg

router = APIRouter()

@router.post("/register", response_model=UserSchema)
async def register(user: UserCreate, db: AsyncSession = Depends(lambda: AsyncSessionLocal())):
    db_user = await get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="С таким именем уже есть пользователь")
    return await create_user(db=db, user=user)

@router.post("/token")
async def login_for_access_token(db: AsyncSession = Depends(lambda: AsyncSessionLocal()), form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Пароль или Имя пользователя не верны",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username},
        secret_key=SECRET_KEY,
        algorithm=ALGORITHM
        )
    return {"access_token": access_token, "token_type": "bearer"}
