from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class NotificationTypeSchema(BaseModel):
    id: int
    code: str
    description: Optional[str]

    class Config:
        orm_mode = True

class UserNotificationSettingSchema(BaseModel):
    notification_type_id: int
    enabled: bool = True
    via_email: bool = True
    via_telegram: bool = False

class NotificationTemplateCreate(BaseModel):
    notification_type_id: int
    channel: str
    subject: Optional[str] = None
    body: str

class NotificationTemplateSchema(NotificationTemplateCreate):
    id: int
    updated_by: Optional[UUID]

    class Config:
        orm_mode = True

class QueueItemCreate(BaseModel):
    notification_type_id: int
    user_id: UUID
    channel: str
    payload: dict
    scheduled_at: Optional[str] = None

class QueueItemSchema(QueueItemCreate):
    id: UUID
    status: str
    attempts: int
    last_error: Optional[str]

    class Config:
        orm_mode = True
