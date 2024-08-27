from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.models import User, Note
from app.schemas import UserCreate, NoteCreate
from app.utils import get_password_hash, correct_spelling, verify_password

async def get_user_by_username(db: AsyncSession, username: str) -> User:
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

async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user