from sqlmodel import Session, select
from models import User, UserCreate, UserResponse
from auth import create_access_token
from typing import Optional
from datetime import timedelta


class AuthService:
    def __init__(self, session: Session):
        self.session = session

    def register_user(self, user_create: UserCreate) -> UserResponse:
        """Register a new user"""
        # Check if user already exists
        existing_user = self.session.exec(
            select(User).where(User.email == user_create.email)
        ).first()

        if existing_user:
            raise ValueError("User with this email already exists")

        # Create new user
        user = User(
            email=user_create.email,
            name=user_create.name
        )
        user.set_password(user_create.password)

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

    def authenticate_user(self, email: str, password: str) -> Optional[UserResponse]:
        """Authenticate user with email and password"""
        user = self.session.exec(
            select(User).where(User.email == email)
        ).first()

        if not user or not user.verify_password(password):
            return None

        return UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

    def create_token_for_user(self, user_id: int) -> str:
        """Create JWT token for user"""
        data = {"sub": str(user_id)}  # Using string as per JWT standard
        token = create_access_token(data=data, expires_delta=timedelta(days=7))
        return token