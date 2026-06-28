# Authentication Module Guide

This note explains the authentication work added to the project in a simple, step-by-step way.

## 1. What was added

The project now has a basic JWT-based authentication flow.

### New files
- app/api/api_v1/routes/auth.py
  - Handles login and current-user lookup.
- app/core/security.py
  - Creates password hashes and JWT tokens.
- app/schemas/auth.py
  - Defines request/response models for auth.
- app/models/user.py
  - Stores the database user record.
- alembic/versions/f4a1b3c2d9e4_create_users_table.py
  - Creates the users table in the database.

## 2. How authentication works

### Login flow
1. The client sends a username and password to /api/auth/login.
2. The server checks the database for the username.
3. If the password matches the stored hash, the server creates a JWT token.
4. The token is returned to the client.

### Protected request flow
1. The client sends the token in the Authorization header.
2. The server decodes the token.
3. If the token is valid, it loads the user from the database.
4. The request continues.

## 3. Important pieces

### Password hashing
Passwords are not stored in plain text.
They are hashed using bcrypt before saving.

### JWT token
A JWT contains a subject claim, usually the username.
It is signed with a secret key so it cannot be forged easily.

## 4. Database changes

A users table was added with these fields:
- id
- username
- hashed_password

A default admin user is created automatically if it does not already exist.

## 5. How to use it

### Login
Send a POST request to:
- /api/auth/login

Use form data:
- username: admin
- password: secret123

### Get current user
Send a GET request to:
- /api/auth/me

Include this header:
- Authorization: Bearer <your_token>

## 6. Run the app
From the project root, start the server with:

```powershell
.\.venv\Scripts\uvicorn.exe app.main:app --reload
```

## 7. What you should learn from this

This project shows how to connect these parts together:
- FastAPI routes
- Pydantic schemas
- SQLAlchemy models
- password hashing
- JWT authentication
- database migrations with Alembic

## 8. Next steps to improve this module

You can extend this later with:
- user registration
- role-based access control
- password reset
- refresh tokens
- email verification
