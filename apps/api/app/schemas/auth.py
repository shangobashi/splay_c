"""Authentication schemas."""
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """User registration request."""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    name: str = Field(..., min_length=2, max_length=100)


class LoginRequest(BaseModel):
    """User login request."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    """User response."""
    id: str
    email: str
    name: str
    subscription_tier: str
    scans_this_month: int
    created_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True


class AuthResponse(BaseModel):
    """Authentication response with user and tokens."""
    user: UserResponse
    tokens: TokenResponse
