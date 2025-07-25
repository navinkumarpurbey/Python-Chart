from fastapi import Depends, HTTPException
from jose import JWTError, jwt  # For encoding/decoding JWT tokens
from passlib.context import CryptContext  # For hashing passwords securely
from sqlalchemy.orm import Session
from . import models, database
from fastapi.security import OAuth2PasswordBearer

# OAuth2 scheme to extract the token from Authorization header (Bearer token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Secret key used to sign JWT tokens (you should keep this secret and secure)
SECRET_KEY = "secret"
ALGORITHM = "HS256"

# Set up bcrypt password hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependency to get a database session; ensures proper connection cleanup
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Verifies that a plain password matches the hashed password from the database
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

# Hashes a plain text password before storing it in the database
def hash_password(password):
    return pwd_context.hash(password)

# Creates a JWT access token from a dictionary of data
def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# Extracts and returns the user's role from the JWT token
def get_user_role(token: str = Depends(...), db: Session = Depends(get_db)):
    try:
        # Decode the token using the secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")  # Subject usually stores the username
        role = payload.get("role")     # Custom claim: role (e.g., admin/user)
        
        # If username is missing, the token is invalid
        if not username:
            raise HTTPException(status_code=401)
        
        return role  # Return the extracted role for RBAC checks

    except JWTError:
        # Raised if the token is invalid or expired
        raise HTTPException(status_code=401)
