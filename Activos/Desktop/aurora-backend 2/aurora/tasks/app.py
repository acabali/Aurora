from celery import Celery
from aurora.core.config import get_settings
settings = get_settings()
celery_app = Celery("aurora", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.task_time_limit = 600
celery_app.conf.result_expires = 3600
@celery_app.task
def ping(): return "pong"
