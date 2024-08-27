from passlib.context import CryptContext
from jose import jwt

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, secret_key: str, algorithm: str):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

# Spellcheck
import httpx

YANDEX_SPELLER_API_URL = "https://speller.yandex.net/services/spellservice.json/checkText"

async def correct_spelling(text: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(YANDEX_SPELLER_API_URL, data={"text": text})
        response.raise_for_status()
        suggestions = response.json()
        for error in suggestions:
            if "s" in error and error["s"]:
                text = text.replace(error["word"], error["s"][0])
        return text