from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any

from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict


class UserRole(str, Enum):
    user = "USER"
    admin = "ADMIN"
    builder = "BUILDER"
    manager_project = "MANAGER_PROJECT"
    manager_catalog = "MANAGER_CATALOG"


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    is_approved: Optional[bool] = None
    role: Optional[UserRole] = None

    # Валидатор для проверки, что хотя бы одно поле заполнено
    @field_validator('*', mode='before')
    @classmethod
    def check_at_least_one_field(cls, v, info: Any):
        if info.field_name != 'password' and v is not None:
            # Устанавливаем флаг, что есть данные для обновления
            if not hasattr(cls, '_has_data'):
                cls._has_data = True
        return v

    @field_validator('password', mode='before')
    @classmethod
    def check_password_or_other_fields(cls, v, info: Any):
        if v is not None:
            if not hasattr(cls, '_has_data'):
                cls._has_data = True
        return v

    # Финальная проверка после валидации всех полей
    @field_validator('*', mode='after')
    @classmethod
    def validate_all_fields(cls, v, info: Any):
        if info.field_name == 'role' and not hasattr(cls, '_has_data'):
            raise ValueError('At least one field must be provided for update')
        return v


# Для смены пароля
class UserChangePassword(BaseModel):
    current_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6)


# Для смены роли
class UserChangeRole(BaseModel):
    role: UserRole


# Для одобрения пользователя
class UserApproveRequest(BaseModel):
    is_approved: bool


class RefreshTokenRequest(BaseModel):
    refresh_token: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user_id: int
    username: str
    role: UserRole


class MessageResponse(BaseModel):
    message: str

class UserResponse(UserBase):
    id: int
    is_approved: bool
    role: UserRole
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)