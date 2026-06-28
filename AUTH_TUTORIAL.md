# Authentication Tutorial for This Project

This tutorial explains the authentication system in a beginner-friendly way.

## 1. What is authentication?

Authentication means verifying who a user is.

In this project, a user logs in with a username and password.
If the credentials are correct, the server gives the user a token.
That token is used later to prove identity.

## 2. What files are involved?

Here is the main flow:

1. The user sends credentials to the login route.
2. The route checks the database.
3. If valid, the server creates a JWT token.
4. The token is used in later requests.

### Main files
- [app/api/api_v1/routes/auth.py](app/api/api_v1/routes/auth.py)
  - Contains the login and current-user endpoints.
- [app/core/security.py](app/core/security.py)
  - Handles hashing and token creation.
- [app/models/user.py](app/models/user.py)
  - Defines the database table for users.
- [app/schemas/auth.py](app/schemas/auth.py)
  - Defines the data shapes used by the auth API.
- [app/db/session.py](app/db/session.py)
  - Creates the database session and startup initialization.

## 3. Step-by-step explanation

### Step 1: User sends login request
The login endpoint receives:
- username
- password

This is handled by the route in [app/api/api_v1/routes/auth.py](app/api/api_v1/routes/auth.py).

### Step 2: The app looks up the user
The route calls a helper that checks the database for the username.

If the user exists, the app compares the provided password with the stored hashed password.

### Step 3: Password hashing
Passwords are never stored as plain text.
They are hashed using bcrypt.

That logic lives in [app/core/security.py](app/core/security.py).

### Step 4: Token creation
If the password matches, the server creates a JWT token.
This token represents the user session.

The token is returned to the client.

### Step 5: Protected route access
Later, when the user calls a protected endpoint, the token is sent in the Authorization header.
The server verifies the token and loads the matching user from the database.

## 4. Why the database is important

The authentication flow is now database-oriented because:
- the user is looked up from the database
- the password hash is stored in the database
- the current user is loaded from the database on protected requests

This is more realistic than keeping everything in memory.

## 5. The user model

The user model is defined in [app/models/user.py](app/models/user.py).

It contains:
- id
- username
- hashed_password

## 6. The auth schema

The schema in [app/schemas/auth.py](app/schemas/auth.py) defines the shape of auth data:
- Token
- TokenData
- UserInfo

This keeps the API input and output organized.

## 7. Example request

### Login request
Send this request:

```http
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=admin&password=secret123
```

### Response
You will receive:

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

## 8. Example protected request

```http
GET /api/auth/me
Authorization: Bearer <token>
```

## 9. How to run the project

From the project root, run:

```powershell
.\.venv\Scripts\uvicorn.exe app.main:app --reload
```

## 10. What you should learn next

To understand this module better, focus on these ideas:
- how FastAPI routes work
- how dependency injection works
- how SQLAlchemy models map to tables
- how JWT tokens are created and verified
- how password hashing improves security

## 11. Suggested practice

Try these exercises:
1. Add a second user to the database.
2. Change the login route to return a clearer message.
3. Add a registration endpoint.
4. Protect another existing route with authentication.
