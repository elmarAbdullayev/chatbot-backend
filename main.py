from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from endpoints import router as endpoints_router
from chatbot import router as chatbot_router

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routen registrieren
app.include_router(endpoints_router)
app.include_router(chatbot_router)
