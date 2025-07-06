from uuid import UUID
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas

async def get_notification_settings(session: AsyncSession, user_id: UUID):
    result = await session.execute(
        select(models.UserNotificationSetting)
        .where(models.UserNotificationSetting.user_id == user_id)
    )
    return result.scalars().all()

async def update_notification_settings(session: AsyncSession, user_id: UUID, settings: list[schemas.UserNotificationSettingSchema]):
    for s in settings:
        await session.execute(
            update(models.UserNotificationSetting)
            .where(models.UserNotificationSetting.user_id == user_id,
                   models.UserNotificationSetting.notification_type_id == s.notification_type_id)
            .values(enabled=s.enabled, via_email=s.via_email, via_telegram=s.via_telegram)
        )
    await session.commit()

async def list_templates(session: AsyncSession, notification_type_id: int | None = None, channel: str | None = None):
    stmt = select(models.NotificationTemplate)
    if notification_type_id:
        stmt = stmt.where(models.NotificationTemplate.notification_type_id == notification_type_id)
    if channel:
        stmt = stmt.where(models.NotificationTemplate.channel == channel)
    result = await session.execute(stmt)
    return result.scalars().all()

async def create_template(session: AsyncSession, data: schemas.NotificationTemplateCreate, user_id: UUID):
    obj = models.NotificationTemplate(
        notification_type_id=data.notification_type_id,
        channel=data.channel,
        subject=data.subject,
        body=data.body,
        updated_by=user_id,
    )
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj

async def update_template(session: AsyncSession, template_id: int, data: schemas.NotificationTemplateCreate, user_id: UUID):
    await session.execute(
        update(models.NotificationTemplate)
        .where(models.NotificationTemplate.id == template_id)
        .values(
            notification_type_id=data.notification_type_id,
            channel=data.channel,
            subject=data.subject,
            body=data.body,
            updated_by=user_id,
        )
    )
    await session.commit()

async def delete_template(session: AsyncSession, template_id: int):
    await session.execute(delete(models.NotificationTemplate).where(models.NotificationTemplate.id == template_id))
    await session.commit()

async def enqueue_notification(session: AsyncSession, item: schemas.QueueItemCreate):
    obj = models.NotificationQueue(
        notification_type_id=item.notification_type_id,
        user_id=item.user_id,
        channel=item.channel,
        payload=item.payload,
        scheduled_at=item.scheduled_at,
    )
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj

async def fetch_queue(session: AsyncSession, status: str = "pending", limit: int = 100):
    result = await session.execute(
        select(models.NotificationQueue).where(models.NotificationQueue.status == status).limit(limit)
    )
    return result.scalars().all()

async def mark_sent(session: AsyncSession, queue_id: UUID):
    await session.execute(
        update(models.NotificationQueue)
        .where(models.NotificationQueue.id == queue_id)
        .values(status="sent")
    )
    await session.commit()

async def mark_failed(session: AsyncSession, queue_id: UUID, error: str):
    await session.execute(
        update(models.NotificationQueue)
        .where(models.NotificationQueue.id == queue_id)
        .values(status="failed", last_error=error, attempts=models.NotificationQueue.attempts + 1)
    )
    await session.commit()
