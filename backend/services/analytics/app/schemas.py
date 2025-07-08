from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Any
import uuid

class ReportTypeOut(BaseModel):
    id: int
    code: str
    description: Optional[str]

    class Config:
        orm_mode = True

class ReportRequestCreate(BaseModel):
    report_type_id: int
    params: Optional[dict] = None

class ReportRequestOut(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    report_type: ReportTypeOut
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ReportScheduleBase(BaseModel):
    report_type_id: int
    frequency: str
    params: Optional[dict]
    active: bool = True

class ReportScheduleOut(ReportScheduleBase):
    id: uuid.UUID
    next_run: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
