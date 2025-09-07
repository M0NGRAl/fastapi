import logging

from celery.result import AsyncResult
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.tasks import add_numbers, process_text
from src.users import user_router
from src.auth import auth_router

app = FastAPI(
    title="My Project API",
    description="Большой проект с модульной структурой",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(auth_router)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.post("/add")
async def add(a: int, b: int):
    """Запуск асинхронной задачи сложения"""
    task = add_numbers.delay(a, b)
    return {"task_id": task.id, "message": "Task started"}


@app.post("/process-text")
async def process_text_endpoint(text: str):
    """Запуск обработки текста"""
    task = process_text.delay(text)
    return {"task_id": task.id, "message": "Text processing started"}


@app.get("/task/{task_id}")
async def get_task_result(task_id: str):
    """Получение результата задачи"""
    task_result = AsyncResult(task_id)

    return {
        "task_id": task_id,
        "status": task_result.state,
        "result": task_result.result if task_result.state == 'SUCCESS' else None,
        "ready": task_result.ready()
    }


@app.get("/health")
async def health_check():
    """Проверка здоровья приложения"""
    return {
        "status": "healthy",
        "services": ["fastapi", "celery", "redis", "postgresql"]
    }
