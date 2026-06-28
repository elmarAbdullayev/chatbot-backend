# Chatbot Backend

A RESTful backend application built with **FastAPI** that provides secure user authentication and AI-powered chatbot functionality. The project was developed as a personal learning project to gain hands-on experience with modern backend development, REST APIs, authentication, Docker, and external AI integrations.

> **Note:** This repository contains only the backend. The React frontend is maintained in a separate repository.

---

## Features

* User registration
* Secure login using JWT authentication
* Password hashing with bcrypt
* Protected API endpoints
* AI chatbot integration via OpenRouter API
* RESTful API architecture
* SQLite database
* CORS configuration for frontend communication
* Docker support for easy deployment

---

## Tech Stack

* Python 3.9
* FastAPI
* Uvicorn
* SQLite
* JWT (python-jose)
* bcrypt
* HTTPX
* Docker
* Python Dotenv

---

## Project Structure

```text
chatbot-backend/
│
├── main.py              # FastAPI application
├── endpoints.py         # Authentication endpoints
├── chatbot.py           # AI chatbot endpoint
├── requirements.txt
├── Dockerfile
└── full_datenbank.db
```

---

## API Endpoints

### Authentication

| Method | Endpoint    | Description                          |
| ------ | ----------- | ------------------------------------ |
| POST   | `/register` | Register a new user                  |
| POST   | `/login`    | Authenticate a user and return a JWT |
| GET    | `/profil`   | Access a protected endpoint          |

### Chatbot

| Method | Endpoint   | Description                                            |
| ------ | ---------- | ------------------------------------------------------ |
| POST   | `/chatbot` | Send messages to the AI chatbot and receive a response |

---

## Getting Started

### Clone the repository

```bash
git clone https://github.com/yourusername/chatbot-backend.git
cd chatbot-backend
```

---

### Install dependencies

```bash
pip install -r requirements.txt
```

---

### Environment Variables

Create a `.env` file inside the project root.

```env
OPENROUTER_API_KEY=your_api_key
YOUR_SITE_URL=http://localhost:8000
YOUR_SITE_NAME=Chatbot Backend
```

---

### Run the application

```bash
uvicorn main:app --reload
```

The API will be available at

```
http://localhost:8000
```

Interactive API documentation:

```
http://localhost:8000/docs
```

---

## Running with Docker

Build the image

```bash
docker build -t chatbot-backend .
```

Run the container

```bash
docker run -p 8000:8000 chatbot-backend
```

---

## Learning Objectives

This project was created to practice:

* Building REST APIs with FastAPI
* User authentication using JWT
* Password security with bcrypt
* Database interaction with SQLite
* Integrating third-party AI APIs
* Asynchronous programming
* Docker containerization
* Backend architecture and routing

---

## Future Improvements

* Refresh Token authentication
* Role-based authorization
* PostgreSQL instead of SQLite
* Unit and integration testing
* Logging
* API rate limiting
* CI/CD pipeline
* Deployment to a cloud platform
* Better error handling
* Environment-based configuration

---

## Security Notice

For security reasons, API keys and other sensitive information should never be stored directly in the source code. They should always be loaded through environment variables.

---

## License

This project was created for educational and portfolio purposes.

---

## Author

Developed as a personal learning project to improve backend development skills using Python and FastAPI.
