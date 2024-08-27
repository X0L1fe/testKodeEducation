from fastapi import FastAPI
from app.routes import auth, notes, misc
from app.database import init_db

app = FastAPI()

# Подключаем маршруты
app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(misc.router)

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/")
async def root():
    return {"message": "ОНО РАБОТАЕТ!"}
