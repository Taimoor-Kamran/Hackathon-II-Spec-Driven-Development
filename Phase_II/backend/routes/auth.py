from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlmodel import Session
from services.auth_service import AuthService
from models import UserCreate, UserResponse
from database import get_session
from typing import Dict
from auth import get_current_user


router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(user_create: UserCreate, session: Session = Depends(get_session)):
    """Register a new user"""
    auth_service = AuthService(session)

    try:
        user = auth_service.register_user(user_create)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login")
def login(email: str = Form(...), password: str = Form(...), session: Session = Depends(get_session)):
    """Login user and return JWT token"""
    auth_service = AuthService(session)

    user = auth_service.authenticate_user(email, password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth_service.create_token_for_user(user.id)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }


@router.get("/me")
def get_current_user_info(token_data: dict = Depends(get_current_user)):
    """Get current user info from token"""
    return {"user_id": token_data.user_id}