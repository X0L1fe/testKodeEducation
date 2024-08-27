from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import NoteCreate, NoteSchema
from app.database import AsyncSessionLocal
from app.crud import create_user_note, get_notes
from app.auth import get_current_user
from app.models import User

router = APIRouter()

@router.post("/notes/", response_model=NoteSchema)
async def create_note(
    note: NoteCreate,
    db: AsyncSession = Depends(lambda: AsyncSessionLocal()),
    current_user: User = Depends(get_current_user),
):
    return await create_user_note(
        db=db, note=note, user_id=current_user.id
    )

@router.get("/notes/", response_model=list[NoteSchema])
async def read_notes(
    db: AsyncSession = Depends(lambda: AsyncSessionLocal()),
    current_user: User = Depends(get_current_user),
):
    return await get_notes(db=db, user_id=current_user.id)
