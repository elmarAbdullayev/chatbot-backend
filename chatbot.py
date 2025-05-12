import os
from fastapi import HTTPException, Request
from pydantic import BaseModel
import httpx  # Moderner als requests für Async
from dotenv import load_dotenv
from fastapi import APIRouter



OLLAMA_API_URL = "http://109.205.160.164:11434/generate"

class Message(BaseModel):
    role: str
    content: str


router = APIRouter()

@router.post("/chatbot")
async def chatbot(request: Request):
    try:
        data = await request.json()
        messages = data.get("messages", [])

        if not messages:
            raise HTTPException(status_code=400, detail="No messages provided")

        # Ollama erwartet ein anderes Format als DeepSeek
        last_message = messages[-1]["content"] if messages else ""

        async with httpx.AsyncClient() as client:
            response = await client.post(
                OLLAMA_API_URL,
                json={
                    "model": "llama3",  # oder "mistral", "gemma" - je nach installiertem Modell
                    "prompt": last_message,
                    "stream": False,  # Für nicht-streaming Antworten
                },
                timeout=30.0,
            )
            response.raise_for_status()
            result = response.json()

        if not result.get("response"):
            raise HTTPException(status_code=500, detail="No response from bot")

        return {"answer": result["response"]}

    except httpx.HTTPStatusError as e:
        error_detail = e.response.json().get("error", {}).get("message", str(e))
        raise HTTPException(status_code=500, detail=f"Ollama API Error: {error_detail}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")