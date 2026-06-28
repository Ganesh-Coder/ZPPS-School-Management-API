# Code-Level Explanation of the Authentication Module

This guide explains the authentication implementation in the project at the code level.

## 1. Entry point: app/main.py

The application starts from [app/main.py](app/main.py).

### What it does
- Creates the FastAPI app
- Adds CORS middleware
- Includes the API router
- Calls the database initialization function

### Important part
```python
app.include_router(api_router, prefix=settings.API_V1_STR)
init_db()
```

This means:
- all API routes are registered
- the database is initialized when the app starts

## 2. API router: app/api/api_v1/api.py

The main API router is defined in [app/api/api_v1/api.py](app/api/api_v1/api.py).

### What it does
It includes all route modules, including the new auth router:

```python
api_router.include_router(auth.router)
```

This makes the auth endpoints available under the main API prefix.

## 3. Auth route file: app/api/api_v1/routes/auth.py

This file contains the login and user profile endpoints.

### Route 1: login
```python
@router.post('/login', response_model=Token)
def login_for_access_token(...):
```

### What happens here
1. The request receives form data with username and password.
2. The helper `authenticate_user` checks the database.
3. If credentials are valid, a JWT is created.
4. The JWT is returned as a response.

### Route 2: current user
```python
@router.get('/me', response_model=UserInfo)
def read_users_me(current_user: UserInfo = Depends(get_current_user)):
```

This route depends on `get_current_user`, which validates the token and returns the current user info.

## 4. Authentication helper: authenticate_user

Inside [app/api/api_v1/routes/auth.py](app/api/api_v1/routes/auth.py), the helper looks like this:

```python
def authenticate_user(*, db: Session, username: str, password: str) -> User | None:
    user = db.query(User).filter(User.username == username).first()
```

### Explanation
- It takes a database session, username, and password.
- It queries the `users` table for a matching username.
- If no user exists, it returns `None`.
- If the password hash matches, it returns the user object.

## 5. Token validation: get_current_user

This function validates the bearer token.

```python
payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
```

### What this means
- The token is decoded using the app secret key.
- The `sub` claim is taken as the username.
- The user is loaded from the database using that username.

If anything fails, a 401 unauthorized error is raised.

## 6. Security helpers: app/core/security.py

This file contains the password and token logic.

### Password hashing
```python
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
```

This uses bcrypt to create a one-way hash.

### Password verification
```python
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

This checks whether the plain password matches the stored hash.

### Token creation
```python
def create_access_token(subject: str | Any, expires_delta: Optional[timedelta] = None) -> str:
```

This function:
- creates an expiration time
- puts the username into the token payload
- signs the token using the secret key

## 7. User model: app/models/user.py

The database model is very simple:

```python
class User(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
```

### Explanation
- `id` is the primary key
- `username` must be unique
- `hashed_password` stores the encrypted password

## 8. Schemas: app/schemas/auth.py

This file defines the API data models.

### Token
```python
class Token(BaseModel):
    access_token: str
    token_type: str
```

### TokenData
```python
class TokenData(BaseModel):
    username: Optional[str] = None
```

### UserInfo
```python
class UserInfo(BaseModel):
    username: str
```

These models make the API responses predictable.

## 9. Database initialization: app/db/session.py

This file creates the SQLAlchemy engine and session factory.

```python
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

### Initialization function
```python
def init_db() -> None:
    Base.metadata.create_all(bind=engine)
```

This creates the tables if they do not exist.

## 10. Why this design works

This authentication flow works because each layer has one role:
- route layer: receives HTTP requests
- service/security layer: handles password and token logic
- model layer: stores user data in the database
- schema layer: defines what data passes in and out

## 11. Important learning points

If you want to understand this code deeply, study these concepts:
- dependency injection in FastAPI
- ORM queries with SQLAlchemy
- password hashing with bcrypt
- JWT token signing and decoding
- how routers are included in FastAPI applications

## 12. Practical exercise

Try modifying these parts:
1. Change the login endpoint to return a different message.
2. Add a registration endpoint.
3. Protect another route with the same auth dependency.
4. Add roles such as `admin` and `user`.
