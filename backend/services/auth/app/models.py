import uuid
from datetime import datetime, timedelta
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, CHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    login_type = Column(String(10), nullable=False)
    phone = Column(String(15), unique=True)
    email = Column(String(255), unique=True)
    password_hash = Column(String(255))
    is_active = Column(Boolean, default=False)
    blocked_until = Column(DateTime)
    email_token = Column(String(36))
    email_token_expires = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class SMSCode(Base):
    __tablename__ = 'sms_codes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(String(15), nullable=False)
    code = Column(CHAR(6), nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)
    attempts = Column(Integer, default=0)

class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    token = Column(CHAR(64), primary_key=True)
    user_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'))
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class PasswordResetToken(Base):
    __tablename__ = 'password_reset_tokens'
    token = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'))
    expires_at = Column(DateTime, nullable=False)
