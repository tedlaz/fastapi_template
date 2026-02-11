# FastAPI template with JWT auth

Minimal FastAPI starter with async SQLAlchemy, JWT auth, and user CRUD basics.

## Features

- FastAPI app with CORS enabled
- Async SQLAlchemy + SQLite (aiosqlite)
- JWT auth with login endpoint
- Password hashing with Argon2 + bcrypt (pwdlib)
- Simple users module with create + me endpoints
- Pytest tests included

## Project structure

```
auth/        Auth routes, schemas, and services
core/        Settings, DB, security helpers
users/       User models, routes, schemas, services
tests/       Pytest tests
main.py      FastAPI app entry
```

## Requirements

- Python >= 3.14
- uv (recommended)

## Setup

1. Install dependencies

```
uv sync
```

2. Configure environment
   Create a `.env` file in the project root if you want to override defaults:

```
DATABASE_URL=sqlite+aiosqlite:///./test.db
SECRET_KEY=change_me_to_a_long_random_secret_key
TOKEN_EXPIRE_MINUTES=60
```

## Run the API

Development (auto-reload):

```
uv run uvicorn main:app --reload
```

Production-like:

```
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

API root:

```
GET /
```

## API overview

Auth

- `POST /auth/login` (form fields: `username`, `password`)

Users

- `POST /users` (JSON: `{ "email": "...", "password": "..." }`)
- `GET /users/me` (Bearer token)

## Example usage

Create a user:

```
curl -X POST http://localhost:8000/users \
	-H "Content-Type: application/json" \
	-d '{"email": "user@example.com", "password": "secret"}'
```

Login for a token:

```
curl -X POST http://localhost:8000/auth/login \
	-H "Content-Type: application/x-www-form-urlencoded" \
	-d "username=user@example.com&password=secret"
```

Use the token:

```
curl http://localhost:8000/users/me \
	-H "Authorization: Bearer <access_token>"
```

## Tests

```
uv run pytest -vs
```
