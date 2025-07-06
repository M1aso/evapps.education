from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID


class SocialBindingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    provider: str
    provider_id: str
    linked_at: datetime



class ProfileBase(BaseModel):
    first_name: str
    nickname: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = Field(None, pattern="^(male|female|other)$")
    country: Optional[str] = None
    city: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None
    experience_id: Optional[int] = None
    avatar_url: Optional[str] = None


class ProfileCreate(ProfileBase):
    user_id: Optional[UUID] = None


class ProfileUpdate(ProfileBase):
    pass


class ProfileOut(ProfileBase):
    model_config = ConfigDict(from_attributes=True)
    user_id: UUID
    social_accounts: List[SocialBindingOut] = []


class ExperienceLevelBase(BaseModel):
    label: str
    sequence: int


class ExperienceLevelOut(ExperienceLevelBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ProfileHistoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    field: str
    old_value: Optional[str]
    new_value: Optional[str]
    changed_at: datetime

