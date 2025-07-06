from sqlalchemy import Column, String, Date, Integer, ForeignKey, DateTime, func, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from .database import Base


class ExperienceLevel(Base):
    __tablename__ = "experience_levels"
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(50), nullable=False)
    sequence = Column(Integer, nullable=False)


class Profile(Base):
    __tablename__ = "profiles"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    nickname = Column(String(50))
    birth_date = Column(Date)
    gender = Column(String(10))
    country = Column(String(100))
    city = Column(String(100))
    company = Column(String(150))
    position = Column(String(150))
    experience_id = Column(Integer, ForeignKey("experience_levels.id"))
    avatar_url = Column(String(255))
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    experience = relationship("ExperienceLevel")
    social_accounts = relationship("SocialBinding", back_populates="profile")


class SocialBinding(Base):
    __tablename__ = "social_bindings"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles.user_id"))
    provider = Column(String(20), nullable=False)
    provider_id = Column(String(255), nullable=False)
    linked_at = Column(DateTime(timezone=True), server_default=func.now())

    profile = relationship("Profile", back_populates="social_accounts")


class ProfileHistory(Base):
    __tablename__ = "profile_history"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles.user_id"))
    field = Column(String(50), nullable=False)
    old_value = Column(Text)
    new_value = Column(Text)
    changed_at = Column(DateTime(timezone=True), server_default=func.now())
    changed_by = Column(UUID(as_uuid=True), nullable=True)

