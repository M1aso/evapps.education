import uuid
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Text, JSON, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .database import Base

class NotificationType(Base):
    __tablename__ = "notification_types"

    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))

class UserNotificationSetting(Base):
    __tablename__ = "user_notification_settings"

    user_id = Column(UUID(as_uuid=True), primary_key=True)
    notification_type_id = Column(Integer, ForeignKey("notification_types.id"), primary_key=True)
    enabled = Column(Boolean, default=True)
    via_email = Column(Boolean, default=True)
    via_telegram = Column(Boolean, default=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    notification_type = relationship("NotificationType")

class NotificationTemplate(Base):
    __tablename__ = "notification_templates"

    id = Column(Integer, primary_key=True)
    notification_type_id = Column(Integer, ForeignKey("notification_types.id"))
    channel = Column(String(10))
    subject = Column(String(255))
    body = Column(Text)
    updated_by = Column(UUID(as_uuid=True))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    notification_type = relationship("NotificationType")

class NotificationQueue(Base):
    __tablename__ = "notification_queue"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    notification_type_id = Column(Integer, ForeignKey("notification_types.id"))
    user_id = Column(UUID(as_uuid=True))
    channel = Column(String(10))
    payload = Column(JSON)
    status = Column(String(10), default="pending")
    attempts = Column(Integer, default=0)
    last_error = Column(Text)
    scheduled_at = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    notification_type = relationship("NotificationType")
