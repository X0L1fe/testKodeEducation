import pytest
from httpx import AsyncClient
import pytest_asyncio
from app.main import app
from app.database import engine, Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

# Настраиваем тестовую сессию
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

@pytest_asyncio.fixture(scope="function")
async def test_db():
    # Создание таблиц перед тестами
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    db_session = TestSessionLocal()
    try:
        yield db_session
    finally:
        await db_session.close()
        # Удаление таблиц после тестов
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post("/register", json={"username": "testuser", "password": "testpassword"})
    print(response.status_code)
    print(response.json())
    assert response.status_code == 200 
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data

@pytest.mark.asyncio
async def test_login_user(client):
    await client.post("/register", json={"username": "testuser", "password": "testpassword"})
    response = await client.post("/token", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
