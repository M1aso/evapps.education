from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import UUID


class SocialBindingOut(BaseModel):
    provider: str
    provider_id: str
    linked_at: datetime

    class Config:
        orm_mode = True


class ProfileBase(BaseModel):
    first_name: str
    nickname: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = Field(None, regex="^(male|female|other)$")
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
    user_id: UUID
    social_accounts: List[SocialBindingOut] = []

    class Config:
        orm_mode = True


class ExperienceLevelBase(BaseModel):
    label: str
    sequence: int


class ExperienceLevelOut(ExperienceLevelBase):
    id: int

    class Config:
        orm_mode = True


class ProfileHistoryOut(BaseModel):
    field: str
    old_value: Optional[str]
    new_value: Optional[str]
    changed_at: datetime

    class Config:
        orm_mode = True

