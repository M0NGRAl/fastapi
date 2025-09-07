from typing import Any, List
from venv import logger

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging
from src.users.models import User, UserRole
from src.users.schemas import UserUpdate, UserChangeRole, UserChangePassword, UserApproveRequest
from src.security import get_password_hash, verify_password, create_access_token, create_refresh_token, verify_token


class UserService:
    @staticmethod
    def get_all_users(db: Session) -> List[User]:
        """Получить всех пользователей"""
        return db.query(User).all()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """Получить пользователя по ID"""
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User:
        """Получить пользователя по username"""
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user


    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User:
        """Обновить данные пользователя"""
        user = UserService.get_user_by_id(db, user_id)

        # Получаем только те поля, которые были переданы (не None)
        update_data = user_data.model_dump(exclude_unset=True)

        if 'password' in update_data:
            update_data['password'] = get_password_hash(update_data['password'])

        for field, value in update_data.items():
            setattr(user, field, value)

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def change_password(db: Session, user_id: int, password_data: UserChangePassword) -> User:
        """Сменить пароль пользователя"""
        user = UserService.get_user_by_id(db, user_id)

        if not verify_password(password_data.current_password, user.password):
            raise HTTPException(status_code=400, detail="Current password is incorrect")

        user.password = get_password_hash(password_data.new_password)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def change_user_role(db: Session, user_id: int, role_data: UserChangeRole) -> User:
        """Изменить роль пользователя (только для админов)"""
        user = UserService.get_user_by_id(db, user_id)
        user.role = role_data.role
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def approve_user(db: Session, user_id: int, approve_data: UserApproveRequest) -> User:
        """Одобрить или отклонить пользователя"""
        user = UserService.get_user_by_id(db, user_id)
        user.is_approved = approve_data.is_approved
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> None:
        """Удалить пользователя"""
        user = UserService.get_user_by_id(db, user_id)
        db.delete(user)
        db.commit()

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> User:
        """Аутентификация пользователя"""
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

