from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from app.utils import verify_password, SECRET_KEY as secret, ALGORITHM as alg, ACCESS_TOKEN_EXPIRE_MINUTES as token

SECRET_KEY = secret
ALGORITHM = alg
ACCESS_TOKEN_EXPIRE_MINUTES = token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def authenticate_user(db: AsyncSession, username: str, password: str):
    from app.crud import get_user_by_username  # Отложенный импорт

    user = await get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

async def get_current_user(db: AsyncSession = Depends(lambda: AsyncSessionLocal()), token: str = Depends(oauth2_scheme)):
    from app.crud import get_user_by_username  # Отложенный импорт

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user