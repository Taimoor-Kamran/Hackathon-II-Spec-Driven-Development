from sqlmodel import Session, select
from models import User, UserCreate, UserResponse
from fastapi import HTTPException, status

class AuthService:
    def __init__(self, session: Session):
        self.session = session

    def register_user(self, user_data: UserCreate) -> UserResponse:
        """Register a new user"""
        # Check if user already exists
        existing_user = self.session.exec(
            select(User).where(User.email == user_data.email)
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        # Create new user
        user = User(
            email=user_data.email,
            name=user_data.name
        )
        user.set_password(user_data.password)

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return self._user_to_response(user)

    def authenticate_user(self, email: str, password: str):
        """Authenticate user credentials"""
        user = self.session.exec(
            select(User).where(User.email == email)
        ).first()

        if not user or not user.verify_password(password):
            return None

        return user

    def _user_to_response(self, user: User) -> UserResponse:
        """Convert User model to UserResponse"""
        return UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at,
            updated_at=user.updated_at
        )