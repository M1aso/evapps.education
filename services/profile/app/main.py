from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
import shutil
import os

from .database import SessionLocal, engine, Base
from . import models, schemas, crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Profile Service")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/profile", response_model=schemas.ProfileOut)
def read_profile(user_id: UUID, db: Session = Depends(get_db)):
    profile = crud.get_profile(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@app.put("/api/profile", response_model=schemas.ProfileOut)
def update_profile(user_id: UUID, profile_update: schemas.ProfileUpdate, db: Session = Depends(get_db)):
    profile = crud.get_profile(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    updated = crud.update_profile(db, profile, profile_update, changed_by=user_id)
    return updated


@app.post("/api/profile/avatar", response_model=dict)
def upload_avatar(user_id: UUID, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(status_code=400, detail="Invalid image type")
    contents = file.file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")
    path = f"avatars/{user_id}_{file.filename}"
    os.makedirs("avatars", exist_ok=True)
    with open(path, "wb") as f:
        f.write(contents)
    profile = crud.get_profile(db, user_id)
    if not profile:
        profile = crud.create_profile(db, schemas.ProfileCreate(user_id=user_id, first_name=""))
    crud.update_profile(db, profile, schemas.ProfileUpdate(avatar_url=path), changed_by=user_id)
    return {"avatar_url": path}


@app.get("/api/experience-levels", response_model=List[schemas.ExperienceLevelOut])
def list_levels(db: Session = Depends(get_db)):
    return crud.list_experience_levels(db)


@app.post("/api/experience-levels", response_model=schemas.ExperienceLevelOut)
def create_level(level: schemas.ExperienceLevelBase, db: Session = Depends(get_db)):
    return crud.create_experience_level(db, level)


@app.put("/api/experience-levels/{level_id}", response_model=schemas.ExperienceLevelOut)
def update_level(level_id: int, level: schemas.ExperienceLevelBase, db: Session = Depends(get_db)):
    updated = crud.update_experience_level(db, level_id, level)
    if not updated:
        raise HTTPException(status_code=404, detail="Not found")
    return updated


@app.delete("/api/experience-levels/{level_id}")
def delete_level(level_id: int, db: Session = Depends(get_db)):
    crud.delete_experience_level(db, level_id)
    return {"ok": True}


@app.post("/api/profile/social/link", response_model=schemas.SocialBindingOut)
def link_social(user_id: UUID, provider: str, provider_id: str, db: Session = Depends(get_db)):
    return crud.link_social(db, user_id, provider, provider_id)


@app.delete("/api/profile/social/{provider}")
def unlink_social(provider: str, user_id: UUID, db: Session = Depends(get_db)):
    crud.unlink_social(db, user_id, provider)
    return {"ok": True}


@app.get("/api/profile/history", response_model=List[schemas.ProfileHistoryOut])
def profile_history(user_id: UUID, page: int = 1, per_page: int = 20, db: Session = Depends(get_db)):
    skip = (page - 1) * per_page
    return crud.list_history(db, user_id, skip=skip, limit=per_page)

