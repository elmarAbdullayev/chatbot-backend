import os
from fastapi import HTTPException, Request
from pydantic import BaseModel
import httpx
from dotenv import load_dotenv
from fastapi import APIRouter

load_dotenv()  # .env dosyasından API anahtarını yükler

router = APIRouter()

# API key sollte NUR in der .env Datei stehen!
OPENROUTER_API_KEY = os.getenv("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")  # Korrekt: Nur der Variablenname
YOUR_SITE_URL = os.getenv("YOUR_SITE_URL", "")  # Optional
YOUR_SITE_NAME = os.getenv("YOUR_SITE_NAME", "")  # Optional

class Message(BaseModel):
    role: str
    content: str

@router.post("/chatbot")
async def chatbot(request: Request):
    try:
        data = await request.json()
        messages = data.get("messages", [])

        if not messages:
            raise HTTPException(status_code=400, detail="No messages provided")

        if not OPENROUTER_API_KEY:
            raise HTTPException(status_code=500, detail="OpenRouter API key not configured")

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }

        if YOUR_SITE_URL:
            headers["HTTP-Referer"] = YOUR_SITE_URL
        if YOUR_SITE_NAME:
            headers["X-Title"] = YOUR_SITE_NAME

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json={
                    "model": "deepseek/deepseek-r1:free",
                    "messages": messages,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            result = response.json()

        answer = result["choices"][0]["message"]["content"]
        return {"answer": answer}

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"OpenRouter API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")