from celery import Celery
import os

# Используем переменные окружения
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

celery_app = Celery(
    'worker',
    broker=redis_url,
    backend=redis_url,
    include=['app.tasks']
)

# Настройки
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Moscow',
    enable_utc=True,
    broker_connection_retry_on_startup=True
)