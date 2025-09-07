from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.users import schemas, services
from src.database import get_db
from src.security import get_current_user
from src.users.models import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[schemas.UserResponse])
def get_all_users(
        db: Session = Depends(get_db),
):
    return services.UserService.get_all_users(db)


@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user_by_id(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):


    return services.UserService.get_user_by_id(db, user_id)



@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(
        user_id: int,
        user_data: schemas.UserUpdate,
        db: Session = Depends(get_db),
):
    return services.UserService.update_user(db, user_id, user_data)


@router.put("/{user_id}/change-password", response_model=schemas.UserResponse)
def change_password(
        user_id: int,
        password_data: schemas.UserChangePassword,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Сменить пароль пользователя"""
    # Пользователь может менять только свой пароль
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return services.UserService.change_password(db, user_id, password_data)


@router.put("/{user_id}/change-role", response_model=schemas.UserResponse)
def change_user_role(
        user_id: int,
        role_data: schemas.UserChangeRole,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Изменить роль пользователя (только для админов)"""
    if current_user.role != schemas.UserRole.admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return services.UserService.change_user_role(db, user_id, role_data)


@router.put("/{user_id}/approve", response_model=schemas.UserResponse)
def approve_user(
        user_id: int,
        approve_data: schemas.UserApproveRequest,
        db: Session = Depends(get_db),
):


    return services.UserService.approve_user(db, user_id, approve_data)


@router.delete("/{user_id}")
def delete_user(
        user_id: int,
        db: Session = Depends(get_db),
):

    services.UserService.delete_user(db, user_id)
    return {"message": "User deleted successfully"}