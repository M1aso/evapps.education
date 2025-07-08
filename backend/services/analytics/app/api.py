from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from .database import get_db
from .models import ReportType, ReportRequest, ReportSchedule
from .schemas import (
    ReportTypeOut,
    ReportRequestCreate,
    ReportRequestOut,
    ReportScheduleBase,
    ReportScheduleOut,
)
from .tasks import generate_report

router = APIRouter(prefix="/api/analytics")

@router.get("/report-types", response_model=list[ReportTypeOut])
def list_report_types(db: Session = Depends(get_db)):
    return db.query(ReportType).all()

@router.post("/reports", response_model=ReportRequestOut)
def request_report(data: ReportRequestCreate, db: Session = Depends(get_db)):
    req = ReportRequest(
        user_id=uuid.uuid4(),  # placeholder, should come from auth context
        report_type_id=data.report_type_id,
        params=data.params,
        status="pending",
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    generate_report.delay(str(req.id))
    return req

@router.get("/reports", response_model=list[ReportRequestOut])
def list_reports(db: Session = Depends(get_db)):
    return db.query(ReportRequest).all()

@router.get("/reports/{request_id}", response_model=ReportRequestOut)
def get_report(request_id: str, db: Session = Depends(get_db)):
    req = db.query(ReportRequest).filter_by(id=request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Not found")
    return req

@router.get("/dashboard")
def dashboard():
    return {"courses": 0, "users": 0, "avg_score": 0}

@router.post("/schedules", response_model=ReportScheduleOut)
def create_schedule(data: ReportScheduleBase, db: Session = Depends(get_db)):
    sched = ReportSchedule(
        user_id=uuid.uuid4(),  # placeholder
        **data.dict(),
    )
    db.add(sched)
    db.commit()
    db.refresh(sched)
    return sched

@router.get("/schedules", response_model=list[ReportScheduleOut])
def list_schedules(db: Session = Depends(get_db)):
    return db.query(ReportSchedule).all()
