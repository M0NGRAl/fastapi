from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.auth import schemas, services
from src.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=schemas.UserResponse)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """Регистрация нового пользователя"""
    try:
        user = services.UserService.create_user(db, user_data)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )


@router.post("/login")
def login(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    """Вход пользователя в систему"""
    try:
        return services.UserService.login_user(db, user_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error logging in"
        )


@router.post("/refresh")
def refresh_tokens(refresh_data: schemas.RefreshTokenRequest):
    """Обновление access и refresh токенов"""
    return services.UserService.refresh_tokens(refresh_data.refresh_token)


@router.post("/logout")
def logout():
    """Выход из системы"""
    return {"message": "Successfully logged out. Please remove tokens from client storage."}
