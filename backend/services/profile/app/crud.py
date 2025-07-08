from sqlalchemy.orm import Session
from . import models, schemas
from typing import List
from uuid import UUID, uuid4


def get_profile(db: Session, user_id: UUID) -> models.Profile:
    return db.query(models.Profile).filter(models.Profile.user_id == user_id).first()


def create_profile(db: Session, profile_in: schemas.ProfileCreate) -> models.Profile:
    profile = models.Profile(
        user_id=profile_in.user_id or uuid4(),
        first_name=profile_in.first_name,
        nickname=profile_in.nickname,
        birth_date=profile_in.birth_date,
        gender=profile_in.gender,
        country=profile_in.country,
        city=profile_in.city,
        company=profile_in.company,
        position=profile_in.position,
        experience_id=profile_in.experience_id,
        avatar_url=profile_in.avatar_url,
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def update_profile(db: Session, profile: models.Profile, update_in: schemas.ProfileUpdate, changed_by: UUID):
    for field, value in update_in.dict(exclude_unset=True).items():
        old_value = getattr(profile, field)
        if value != old_value:
            setattr(profile, field, value)
            history = models.ProfileHistory(
                user_id=profile.user_id,
                field=field,
                old_value=str(old_value) if old_value is not None else None,
                new_value=str(value) if value is not None else None,
                changed_by=changed_by,
            )
            db.add(history)
    db.commit()
    db.refresh(profile)
    return profile


def list_experience_levels(db: Session) -> List[models.ExperienceLevel]:
    return db.query(models.ExperienceLevel).order_by(models.ExperienceLevel.sequence).all()


def create_experience_level(db: Session, level: schemas.ExperienceLevelBase) -> models.ExperienceLevel:
    obj = models.ExperienceLevel(label=level.label, sequence=level.sequence)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_experience_level(db: Session, exp_id: int, level: schemas.ExperienceLevelBase) -> models.ExperienceLevel:
    obj = db.query(models.ExperienceLevel).get(exp_id)
    if not obj:
        return None
    obj.label = level.label
    obj.sequence = level.sequence
    db.commit()
    db.refresh(obj)
    return obj


def delete_experience_level(db: Session, exp_id: int):
    obj = db.query(models.ExperienceLevel).get(exp_id)
    if obj:
        db.delete(obj)
        db.commit()


def link_social(db: Session, user_id: UUID, provider: str, provider_id: str) -> models.SocialBinding:
    binding = models.SocialBinding(user_id=user_id, provider=provider, provider_id=provider_id)
    db.add(binding)
    db.commit()
    db.refresh(binding)
    return binding


def unlink_social(db: Session, user_id: UUID, provider: str):
    binding = db.query(models.SocialBinding).filter_by(user_id=user_id, provider=provider).first()
    if binding:
        db.delete(binding)
        db.commit()


def list_history(db: Session, user_id: UUID, skip: int = 0, limit: int = 20) -> List[models.ProfileHistory]:
    return (
        db.query(models.ProfileHistory)
        .filter(models.ProfileHistory.user_id == user_id)
        .order_by(models.ProfileHistory.changed_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
