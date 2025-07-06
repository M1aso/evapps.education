import uuid
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, JSON, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .database import Base

class ReportType(Base):
    __tablename__ = "report_types"

    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True)
    description = Column(String(255))

    requests = relationship("ReportRequest", back_populates="report_type")

class ReportRequest(Base):
    __tablename__ = "report_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True))
    report_type_id = Column(Integer, ForeignKey("report_types.id"))
    params = Column(JSON)
    status = Column(String(10))
    error = Column(Text)
    created_at = Column(TIMESTAMP, server_default="now()")
    updated_at = Column(TIMESTAMP, server_default="now()")

    report_type = relationship("ReportType", back_populates="requests")
    result = relationship("ReportResult", uselist=False, back_populates="request")

class ReportResult(Base):
    __tablename__ = "report_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(UUID(as_uuid=True), ForeignKey("report_requests.id"))
    format = Column(String(10))
    file_url = Column(Text)
    size_bytes = Column(Integer)
    created_at = Column(TIMESTAMP, server_default="now()")

    request = relationship("ReportRequest", back_populates="result")

class ReportSchedule(Base):
    __tablename__ = "report_schedules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True))
    report_type_id = Column(Integer, ForeignKey("report_types.id"))
    frequency = Column(String(10))
    next_run = Column(TIMESTAMP)
    active = Column(Boolean, default=True)
    params = Column(JSON)
    created_at = Column(TIMESTAMP, server_default="now()")
    updated_at = Column(TIMESTAMP, server_default="now()")

    report_type = relationship("ReportType")
