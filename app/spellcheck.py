import httpx

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
