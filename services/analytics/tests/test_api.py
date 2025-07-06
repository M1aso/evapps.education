import os
import sys
import uuid
from pathlib import Path
from fastapi.testclient import TestClient

# Ensure package imports work when running via pytest
sys.path.append(str(Path(__file__).resolve().parents[3]))

DB_PATH = "analytics_test.db"
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
os.environ.setdefault("ANALYTICS_DATABASE_URL", f"sqlite:///{DB_PATH}")
os.environ.setdefault("RABBITMQ_URL", "memory://")

from services.analytics.app.main import app
from services.analytics.app.database import Base, engine, SessionLocal
from services.analytics.app import models

Base.metadata.create_all(bind=engine)
client = TestClient(app)

def test_dashboard():
    resp = client.get("/api/analytics/dashboard")
    assert resp.status_code == 200
    assert set(resp.json().keys()) == {"courses", "users", "avg_score"}

def test_request_report():
    db = SessionLocal()
    if not db.query(models.ReportType).filter_by(id=1).first():
        db.add(models.ReportType(id=1, code="basic"))
        db.commit()
    resp = client.post("/api/analytics/reports", json={"report_type_id": 1, "params": {}})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "pending"
    db.close()
