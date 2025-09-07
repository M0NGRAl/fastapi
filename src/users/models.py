from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum as PyEnum
from src.database import Base

class UserRole(PyEnum):
    USER = "USER"
    ADMIN = "ADMIN"
    BUILDER = "BUILDER"
    MANAGER_PROJECT = "MANAGER_PROJECT"
    MANAGER_CATALOG = "MANAGER_CATALOG"

# Создаем ENUM тип для PostgreSQL
user_role_enum = ENUM(
    UserRole,
    name="user_role",
    create_type=False,  # Установите True если тип еще не создан в БД
    values_callable=lambda x: [e.value for e in x]  # Важно: возвращаем значения, а не enum objects
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_approved = Column(Boolean, default=False, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(user_role_enum, default=UserRole.USER.value, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"