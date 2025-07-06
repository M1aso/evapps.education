import os
import uuid
from celery import Celery
from jinja2 import Template
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from .config import get_settings
from .database import SessionLocal
from .models import ReportRequest, ReportResult

settings = get_settings()
celery_app = Celery('analytics', broker=settings.rabbitmq_url)

@celery_app.task
def generate_report(request_id: str):
    db = SessionLocal()
    try:
        req = db.query(ReportRequest).filter_by(id=request_id).first()
        if not req:
            return
        # Placeholder: generate dummy data
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer)
        styles = getSampleStyleSheet()
        story = [Paragraph("Example report", styles['Title'])]
        doc.build(story)
        file_id = uuid.uuid4()
        file_path = f"reports/{file_id}.pdf"
        os.makedirs("reports", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(pdf_buffer.getvalue())
        result = ReportResult(
            id=file_id,
            request_id=req.id,
            format="pdf",
            file_url=file_path,
            size_bytes=len(pdf_buffer.getvalue()),
        )
        req.status = "ready"
        db.add(result)
        db.commit()
    except Exception as exc:
        if req:
            req.status = "failed"
            req.error = str(exc)
            db.commit()
        raise
    finally:
        db.close()
