from typing import Any, List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from src.auth.schemas import UserCreate, UserLogin
from src.users.models import User
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
    def create_user(db: Session, user_data: UserCreate) -> User:
        """Создать нового пользователя"""
        try:
            if db.query(User).filter(User.username == user_data.username).first():
                raise HTTPException(status_code=400, detail="Username already taken")

            if db.query(User).filter(User.email == user_data.email).first():
                raise HTTPException(status_code=400, detail="Email already taken")

            hashed_password = get_password_hash(user_data.password)

            db_user = User(
                username=user_data.username,
                email=user_data.email,
                password=hashed_password,
                role=user_data.role
            )

            db.add(db_user)
            db.commit()
            db.refresh(db_user)

            return db_user

        except HTTPException:
            db.rollback()
            raise
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail="Database integrity error")
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error occurred"
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating user"
            )


    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> User:
        """Аутентификация пользователя"""
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    @staticmethod
    def login_user(db: Session, user_data: UserLogin) -> dict:
        """Вход пользователя в систему"""
        user = UserService.authenticate_user(db, user_data.username, user_data.password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")


        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user_id": user.id,
            "username": user.username,
            "role": user.role.value
        }

    @staticmethod
    def verify_user(db: Session, VerifyToken):
        payload = verify_token(VerifyToken.token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")
        

    @staticmethod
    def refresh_tokens(refresh_token: str) -> dict:
        """Обновление access и refresh токенов"""
        payload = verify_token(refresh_token, "refresh")
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user_id = payload.get("sub")
        new_access_token = create_access_token({"sub": user_id})
        new_refresh_token = create_refresh_token({"sub": user_id})

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }