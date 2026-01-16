"""Authentication routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    AuthResponse,
    UserResponse,
    TokenResponse,
)
from app.services import auth as auth_service

router = APIRouter()


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user.

    Args:
        request: Registration request with email, password, and name
        db: Database session

    Returns:
        AuthResponse with user and tokens

    Raises:
        HTTPException: If email already exists
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "EMAIL_EXISTS", "message": "Email already registered"}
        )

    # Create new user
    user = User(
        email=request.email,
        password_hash=auth_service.hash_password(request.password),
        name=request.name,
        subscription_tier="free",
        scans_this_month=0,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # Generate tokens
    access_token = auth_service.create_access_token({"sub": user.id})
    refresh_token = auth_service.create_refresh_token({"sub": user.id})

    return AuthResponse(
        user=UserResponse.model_validate(user),
        tokens=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=15 * 60,  # 15 minutes
        ),
    )


@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return tokens.

    Args:
        request: Login request with email and password
        db: Database session

    Returns:
        AuthResponse with user and tokens

    Raises:
        HTTPException: If credentials are invalid
    """
    # Find user by email
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "INVALID_CREDENTIALS", "message": "Invalid email or password"}
        )

    # Verify password
    if not auth_service.verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "INVALID_CREDENTIALS", "message": "Invalid email or password"}
        )

    # Generate tokens
    access_token = auth_service.create_access_token({"sub": user.id})
    refresh_token = auth_service.create_refresh_token({"sub": user.id})

    return AuthResponse(
        user=UserResponse.model_validate(user),
        tokens=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=15 * 60,  # 15 minutes
        ),
    )


@router.get("/test")
async def test():
    """Test endpoint to verify auth router is working."""
    return {"message": "Auth routes working!", "endpoints": ["/register", "/login"]}
