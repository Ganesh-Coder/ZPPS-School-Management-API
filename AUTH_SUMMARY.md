# Auth Module Summary

## Purpose
This module adds login and token-based authentication to the FastAPI app.

## Main pieces
- Login endpoint: /api/auth/login
- Current user endpoint: /api/auth/me
- Token type: JWT
- Password hashing: bcrypt

## Files
- app/api/api_v1/routes/auth.py
  - Handles login and token validation
- app/core/security.py
  - Creates hashes and JWTs
- app/models/user.py
  - Stores user data in the database
- app/schemas/auth.py
  - Defines auth request/response models
- app/db/session.py
  - Creates DB sessions and startup initialization

## Flow
1. Client sends username and password.
2. Server finds the user in the database.
3. Server checks the password hash.
4. Server creates a JWT token.
5. Client sends the token in the Authorization header.
6. Server validates the token and loads the user.

## Default credentials
- Username: admin
- Password: secret123

## Run command
```powershell
.\.venv\Scripts\uvicorn.exe app.main:app --reload
```

## Learning focus
- FastAPI routes
- Dependency injection
- SQLAlchemy ORM
- JWT
- Password hashing
