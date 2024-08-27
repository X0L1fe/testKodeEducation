from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import NoteCreate, NoteSchema, NoteUpdate
from app.database import AsyncSessionLocal
from app.crud import create_user_note, delete_user_note, get_notes, update_user_note
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

@router.delete("/notes/{note_id}", response_model=bool)
async def delete_note(
    note_id: int,
    db: AsyncSession = Depends(lambda: AsyncSessionLocal()),
    current_user: User = Depends(get_current_user)):
    success = await delete_user_note(db, note_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found or not authorized")
    return success

@router.put("/notes/{note_id}", response_model=NoteSchema)
async def update_note(
    note_id: int,
    note_update: NoteUpdate,
    db: AsyncSession = Depends(lambda: AsyncSessionLocal()),
    current_user: User = Depends(get_current_user)):
    updated_note = await update_user_note(
        db, note_id, current_user.id, title=note_update.title, content=note_update.content
    )
    if not updated_note:
        raise HTTPException(status_code=404, detail="Note not found or not authorized")
    return updated_note