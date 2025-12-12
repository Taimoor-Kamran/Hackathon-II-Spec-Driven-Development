from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from sqlmodel import Session, select
from models import User
from database import get_session

# Load environment variables
load_dotenv()

# Initialize JWT
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# Security schemes
security = HTTPBearer()

class TokenData(BaseModel):
    user_id: int  # Changed from str to int
    email: Optional[str] = None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create an access token with expiration"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[TokenData]:
    """Verify and decode a JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str: str = payload.get("sub")
        email: str = payload.get("email")

        if user_id_str is None:
            return None

        # Convert user_id from string to int
        try:
            user_id = int(user_id_str)
        except ValueError:
            return None

        token_data = TokenData(user_id=user_id, email=email)
        return token_data
    except JWTError:
        return None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), session: Session = Depends(get_session)):
    """Get current user from JWT token in Authorization header"""
    token = credentials.credentials
    token_data = verify_token(token)

    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get the actual user from the database to verify they exist
    user = session.exec(select(User).where(User.id == token_data.user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token_data

def verify_user_id_match(token_user_id: int, url_user_id: str) -> bool:
    """Verify that the user ID in the token matches the user ID in the URL"""
    # Convert URL user_id to int for comparison
    try:
        url_user_id_int = int(url_user_id)
        return token_user_id == url_user_id_int
    except ValueError:
        return False  # If URL user_id is not a valid integer, it can't match