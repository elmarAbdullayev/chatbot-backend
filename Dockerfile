# Benutze ein Python-Image als Basis
FROM python:3.9

# Setze das Arbeitsverzeichnis
WORKDIR /app

# Kopiere requirements.txt
COPY requirements.txt .

# Installiere die Abhängigkeiten
RUN pip install -r requirements.txt

# Kopiere den gesamten Code
COPY . .

# Exponiere den Port für FastAPI
EXPOSE 8000

# Starte den FastAPI-Server
CMD ["uvicorn", "endpoints:app", "--host", "0.0.0.0", "--port", "8000"]

