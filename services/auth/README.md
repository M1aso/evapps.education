# Auth Service

A FastAPI-based microservice implementing the authentication module described in `REQUIREMENTS.md`.

## Features
- Phone registration and login with SMS verification
- Email registration with confirmation link
- Email and phone login issuing JWT access and refresh tokens
- Password reset via email
- Logout by invalidating refresh tokens

## Setup

Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the service:
```bash
uvicorn app.main:app --reload
```

Environment variables can be defined in `.env` or exported in the shell. See `.env.example` in the repository root for common variables.
