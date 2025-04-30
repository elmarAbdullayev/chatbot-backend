import bcrypt
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm ## OAuth2PasswordBearer Dieser wird verwendet, um den Token aus der Anfrage zu extrahieren.   Damit # #####OAuth2PasswordRequestForm enthalten wir username und password.
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.middleware.cors import CORSMiddleware




# Fake-Datenbank
fake_user_db = {
    "test@example.com": {
        "email": "test@example.com",
        "hashed_password": bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt())
    }
}

fake_profil_data = {
    "privatdata" : {
        "name":"elmar",
        "age":29,
        "job":"developer"
    },
    "programmlanguages":{
        "first":"javaa",
        "second":"python"
    }
}
# Geheimschlüssel und Token-Algorithmus
SECRET_KEY = "mein_geheimes_token"  # In echt: gut schützen!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Item(BaseModel):
    email: str
    password: str

# OAuth2Bearer-Schema
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# FastAPI-Instanz
app = FastAPI()

# CORS einrichten, um Anfragen vom Frontend zu erlauben
origins = [
    "http://localhost:3000",  # React Frontend-Adresse
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Passwort verifizieren
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

# Token erstellen
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Login Route: POST, weil wir Login-Daten senden
@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_user_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Falsche Email oder Passwort")
    token = create_access_token(data={"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer"}


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except JWTError:
        return False

# Profil Route
@app.get("/profil")
async def profil(token:str = Depends(oauth2_scheme)): ## Token wird automatisch aus dem Header gelesen.
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Ungültiger Token")

    return {"message": "Erfolgreich authentifiziert", "data": fake_profil_data}


# Register Route
@app.post("/register")
async def register(info: Item):
    # Hier könntest du Benutzerdaten speichern oder weiter verarbeiten
    return {"message": "User registriert", "user": info}
