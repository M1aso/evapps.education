from .config import get_settings
from .tasks import celery_app

settings = get_settings()
__all__ = ["settings", "celery_app"]
