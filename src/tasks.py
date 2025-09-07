from .celery_app import celery_app
import time

@celery_app.task
def add_numbers(a: int, b: int) -> int:
    """Простая задача сложения чисел"""
    time.sleep(5)  # Имитация долгой операции
    return a + b

@celery_app.task
def process_text(text: str) -> dict:
    """Обработка текста"""
    time.sleep(3)
    return {
        'original': text,
        'length': len(text),
        'uppercase': text.upper(),
        'processed_at': time.time()
    }