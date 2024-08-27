import pytest
from httpx import AsyncClient
from app.main import app
from app.database import engine, Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

@pytest.fixture(scope="function")
async def test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield TestSessionLocal
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def client(test_db):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_create_note(client):
    # Регистрация и логин
    await client.post("/register", json={"username": "testuser", "password": "testpassword"})
    login_response = await client.post("/token", data={"username": "testuser", "password": "testpassword"})
    token = login_response.json()["access_token"]

    # Создание заметки
    response = await client.post("/notes/", json={"title": "Test Note", "content": "This is a test note"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Note"
    assert data["content"] == "This is a test note"

@pytest.mark.asyncio
async def test_read_notes(client):
    await client.post("/register", json={"username": "testuser", "password": "testpassword"})
    login_response = await client.post("/token", data={"username": "testuser", "password": "testpassword"})
    token = login_response.json()["access_token"]

    await client.post("/notes/", json={"title": "Test Note", "content": "This is a test note"}, headers={"Authorization": f"Bearer {token}"})

    response = await client.get("/notes/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Note"
