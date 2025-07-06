import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID
from typing import List

from .database import get_session, Base, engine
from . import crud, schemas, models

app = FastAPI(title="Notification Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/api/notifications/settings", response_model=List[schemas.UserNotificationSettingSchema])
async def get_settings(user_id: UUID, session=Depends(get_session)):
    return await crud.get_notification_settings(session, user_id)

@app.put("/api/notifications/settings")
async def update_settings(user_id: UUID, data: List[schemas.UserNotificationSettingSchema], session=Depends(get_session)):
    await crud.update_notification_settings(session, user_id, data)
    return {"status": "ok"}

@app.get("/api/notifications/templates", response_model=List[schemas.NotificationTemplateSchema])
async def list_templates(notification_type_id: int | None = None, channel: str | None = None, session=Depends(get_session)):
    return await crud.list_templates(session, notification_type_id, channel)

@app.post("/api/notifications/templates", response_model=schemas.NotificationTemplateSchema)
async def create_template(data: schemas.NotificationTemplateCreate, session=Depends(get_session)):
    user_id = UUID("00000000-0000-0000-0000-000000000001")
    return await crud.create_template(session, data, user_id)

@app.put("/api/notifications/templates/{template_id}")
async def update_template(template_id: int, data: schemas.NotificationTemplateCreate, session=Depends(get_session)):
    user_id = UUID("00000000-0000-0000-0000-000000000001")
    await crud.update_template(session, template_id, data, user_id)
    return {"status": "ok"}

@app.delete("/api/notifications/templates/{template_id}")
async def delete_template(template_id: int, session=Depends(get_session)):
    await crud.delete_template(session, template_id)
    return {"status": "ok"}

@app.post("/internal/notifications/enqueue", response_model=schemas.QueueItemSchema)
async def enqueue(data: schemas.QueueItemCreate, session=Depends(get_session)):
    return await crud.enqueue_notification(session, data)

@app.get("/internal/notifications/queue", response_model=List[schemas.QueueItemSchema])
async def list_queue(status: str = "pending", limit: int = 100, session=Depends(get_session)):
    return await crud.fetch_queue(session, status, limit)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
