from src.users.schemas import UserBase, UserRole
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any

from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict

class UserResponse(UserBase):
    id: int
    is_approved: bool
    role: UserRole
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class VerifyToken(BaseModel):
    token: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user_id: int
    username: str
    role: UserRole


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    role: UserRole = Field(default=UserRole.user)


class UserLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)