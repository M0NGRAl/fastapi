import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

load_dotenv()

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


async def test_connection():
    try:
        # Создаем engine для теста
        engine = create_async_engine(
            SQLALCHEMY_DATABASE_URL,
            echo=True,
            future=True
        )

        # Пробуем подключиться
        async with engine.connect() as conn:
            # Выполняем простой запрос
            result = await conn.execute(text("SELECT version();"))
            version = result.scalar()
            print(f"✅ Подключение успешно! Версия PostgreSQL: {version}")

            # Проверяем доступность базы данных
            result = await conn.execute(text("SELECT current_database();"))
            db_name = result.scalar()
            print(f"✅ База данных: {db_name}")

            # Проверяем список баз данных
            result = await conn.execute(text("SELECT datname FROM pg_database;"))
            databases = [row[0] for row in result.fetchall()]
            print(f"✅ Доступные базы данных: {databases}")

        await engine.dispose()
        return True

    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False


if __name__ == "__main__":
    # Запускаем тест
    success = asyncio.run(test_connection())
    exit(0 if success else 1)