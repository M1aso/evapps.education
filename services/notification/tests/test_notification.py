import os
import sys
import uuid
import asyncio
from pathlib import Path
from fastapi.testclient import TestClient

# Add repository root to the path so ``services`` can be imported as a package
ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

DB_PATH = "notification_test.db"
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
os.environ.setdefault("NOTIFICATION_DATABASE_URL", f"sqlite+aiosqlite:///{DB_PATH}")

from services.notification.app.main import app
from services.notification.app.database import engine, Base, AsyncSessionLocal
from services.notification.app import models

async def _init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        if not await session.get(models.NotificationType, 1):
            session.add(models.NotificationType(id=1, code="test"))
            await session.commit()

asyncio.get_event_loop().run_until_complete(_init_db())
client = TestClient(app)

def test_enqueue_and_list():
    resp = client.get("/internal/notifications/queue")
    assert resp.status_code == 200
    assert resp.json() == []

    data = {
        "notification_type_id": 1,
        "user_id": str(uuid.uuid4()),
        "channel": "email",
        "payload": {},
    }
    resp = client.post("/internal/notifications/enqueue", json=data)
    assert resp.status_code == 200
    assert resp.json()["status"] == "pending"
