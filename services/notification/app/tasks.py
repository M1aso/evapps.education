import os
from celery import Celery
import asyncio
from .database import AsyncSessionLocal
from . import crud

CELERY_BROKER = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
CELERY_BACKEND = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery("notification", broker=CELERY_BROKER, backend=CELERY_BACKEND)

@celery_app.task
def send_notification(queue_id: str):
    async def _send():
        async with AsyncSessionLocal() as session:
            from uuid import UUID
            try:
                await crud.mark_sent(session, UUID(queue_id))
            except Exception as e:
                await crud.mark_failed(session, UUID(queue_id), str(e))

    asyncio.run(_send())
