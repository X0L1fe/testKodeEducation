from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import AsyncSessionLocal

router = APIRouter()

@router.get("/ping-db")
async def ping_db(db: AsyncSession = Depends(lambda: AsyncSessionLocal())):
    try:
        result = await db.execute(text("SELECT 1"))
        return {"status": "Connected"}
    except Exception as e:
        return {"status": "Failed", "reason": str(e)}
