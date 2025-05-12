import bcrypt
from fastapi import HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import jwt, JWTError
import sqlite3
from fastapi import APIRouter


# Datenbank vorbereiten
with sqlite3.connect("full_datenbank.db") as conn:
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)
    conn.commit()

router = APIRouter()

# Token-Einstellungen
SECRET_KEY = "mein_geheimes_token"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Modelle
class RegisterData(BaseModel):
    name: str
    email: str
    password: str
    role: str

# OAuth2-Konfiguration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Passwortprüfung
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

# Token-Erstellung
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Token prüfen
def verify_token(token: str):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except JWTError:
        return False

# E-Mail prüfen
def email_exists(email):
    with sqlite3.connect("full_datenbank.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()
        return result is not None

# Benutzer aus DB laden
def get_user_by_email(email):
    with sqlite3.connect("full_datenbank.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT email, password FROM users WHERE email = ?", (email,))
        return cursor.fetchone()

# Registrieren
@router.post("/register")
async def register(info: RegisterData):
    if email_exists(info.email):
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_password = bcrypt.hashpw(info.password.encode('utf-8'), bcrypt.gensalt())

    with sqlite3.connect("full_datenbank.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
            (info.name, info.email, hashed_password, info.role)
        )
        conn.commit()

    return {"message": "User registriert", "user": info}

# Login
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    result = get_user_by_email(form_data.username)
    if not result:
        raise HTTPException(status_code=401, detail="Falsche Email oder Passwort")

    email, hashed_password = result
    if not verify_password(form_data.password, hashed_password):
        raise HTTPException(status_code=401, detail="Falsche Email oder Passwort")

    token = create_access_token(data={"sub": email})
    return {"access_token": token, "token_type": "bearer"}

# Geschützte Route
@router.get("/profil")
async def profil(token: str = Depends(oauth2_scheme)):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Ungültiger Token")

    return {"message": "Erfolgreich authentifiziert", "data": fake_profil_data}
