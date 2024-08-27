from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import Column, Integer, String, ForeignKey, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import relationship, sessionmaker, joinedload, declarative_base, configure_mappers
from sqlalchemy.future import select
from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import BaseModel
import httpx


# Configurations
DATABASE_URL = "postgresql+asyncpg://postgres:password@127.0.0.1:5432/KodeEducation"


SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database setup
Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

#Tables setup
async def init_db():
    async with engine.begin() as conn:
        await conn.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL
        )
        """))

        await conn.execute(text("""
        CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            content TEXT,
            owner_id INTEGER REFERENCES users(id) ON DELETE CASCADE
        )
        """))

        await conn.commit()

# Модели
class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))

    # Замедленная загрузка класса User
    owner = relationship('User', back_populates='notes', lazy='joined')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    # Замедленная загрузка класса Note
    notes = relationship('Note', back_populates='owner', lazy='joined')

# Принудительная конфигурация мапперов
configure_mappers()

# Schemas NOTE
class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    pass

class NoteSchema(NoteBase):
    id: int
    owner_id: int
    class Config:
        from_attributes = True

# Schemas USER
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserSchema(UserBase):  # Это схема для Pydantic
    id: int

    class Config:
        from_attributes = True  # Изменено на from_attributes вместо orm_mode


# Authentication
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

async def get_current_user(db: AsyncSession = Depends(lambda: AsyncSessionLocal()), token: str = Depends(oauth2_scheme)):
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

def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# CRUD Operations
async def get_user_by_username(db: AsyncSession, username: str) -> User:
    # Используем select(User) вместо select(User.username == username)
    query = select(User).where(User.username == username).options(joinedload(User.notes))
    result = await db.execute(query)
    user = result.scalars().first()
    return user


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def create_user_note(
    db: AsyncSession, note: NoteCreate, user_id: int
) -> Note:
    corrected_text = await correct_spelling(note.content)
    db_note = Note(title=note.title, content=corrected_text, owner_id=user_id)
    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    return db_note

async def get_notes(db: AsyncSession, user_id: int):
    query = select(Note).filter(Note.owner_id == user_id)
    result = await db.execute(query)
    return result.unique().scalars().all()

# Spellcheck
YANDEX_SPELLER_API_URL = "https://speller.yandex.net/services/spellservice.json/checkText"

async def check_spelling(text: str) -> list[str]:
    async with httpx.AsyncClient() as client:
        response = await client.post(YANDEX_SPELLER_API_URL, data={"text": text})
        response.raise_for_status()
        suggestions = response.json()
        errors = [error["word"] for error in suggestions if "word" in error]
        return errors

async def correct_spelling(text: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(YANDEX_SPELLER_API_URL, data={"text": text})
        response.raise_for_status()
        suggestions = response.json()
        for error in suggestions:
            if "s" in error and error["s"]:
                text = text.replace(error["word"], error["s"][0])
        return text

# FastAPI app setup
app = FastAPI()

# Routers
@app.post("/register", response_model=UserSchema)
async def register(user: UserCreate, db: AsyncSession = Depends(lambda: AsyncSessionLocal())):
    db_user = await get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return await create_user(db=db, user=user)

@app.post("/token")
async def login_for_access_token(db: AsyncSession = Depends(lambda: AsyncSessionLocal()), form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/notes/", response_model=NoteSchema)
async def create_note(
    note: NoteCreate,
    db: AsyncSession = Depends(lambda: AsyncSessionLocal()),
    current_user: User = Depends(get_current_user),
):
    return await create_user_note(
        db=db, note=note, user_id=current_user.id
    )

@app.get("/notes/", response_model=list[NoteSchema])
async def read_notes(
    db: AsyncSession = Depends(lambda: AsyncSessionLocal()),
    current_user: User = Depends(get_current_user),
):
    return await get_notes(db=db, user_id=current_user.id)

@app.get("/ping-db")
async def ping_db(db: AsyncSession = Depends(lambda: AsyncSessionLocal())):
    try:
        result = await db.execute(text("SELECT 1"))
        return {"status": "Connected"}
    except Exception as e:
        return {"status": "Failed", "reason": str(e)}

@app.get("/")
async def root():
    return {"message": "Welcome to the Notes API!"}

@app.on_event("startup")
async def on_startup():
    await init_db()