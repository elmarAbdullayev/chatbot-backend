import os
from fastapi import HTTPException, Request
from pydantic import BaseModel
import httpx
from dotenv import load_dotenv
from fastapi import APIRouter

#load_dotenv()  # Lädt Umgebungsvariablen aus .env Datei

router = APIRouter()

# Konfiguration aus Umgebungsvariablen
OPENROUTER_API_KEY = "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"
YOUR_SITE_URL = os.getenv("YOUR_SITE_URL", "https://chatbot-backend-uu0i.onrender.com")  # Optional
YOUR_SITE_NAME = os.getenv("YOUR_SITE_NAME", "Mein FastApi ChatBot")  # Optional


class Message(BaseModel):
    role: str
    content: str


@router.post("/chatbot")
async def chatbot(request: Request):
    try:
        # Nachrichten vom Request erhalten
        data = await request.json()
        messages = data.get("messages", [])

        # Validierung der Eingabe
        if not messages:
            raise HTTPException(status_code=400, detail="Keine Nachrichten erhalten")

        if not OPENROUTER_API_KEY:
            raise HTTPException(status_code=500, detail="OpenRouter API Key nicht konfiguriert")

        # Header nach Muster-Code Struktur
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": YOUR_SITE_URL,
            "X-Title": YOUR_SITE_NAME
        }

        # Request-Daten nach Muster-Code Struktur
        request_data = {
            "model": "deepseek/deepseek-r1:free",
            "messages": messages
        }

        # API-Aufruf mit httpx (asynchrone Version von requests)
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=request_data,
                timeout=30.0
            )
            response.raise_for_status()
            result = response.json()

        # Antwort verarbeiten
        answer = result["choices"][0]["message"]["content"]
        return {"answer": answer}

    except httpx.HTTPStatusError as e:
        error_detail = f"OpenRouter API Fehler: {str(e)}"
        if e.response.status_code == 401:
            error_detail = "Ungültiger API-Key oder nicht autorisiert"
        raise HTTPException(
            status_code=e.response.status_code,
            detail=error_detail
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Interner Serverfehler: {str(e)}"
        )