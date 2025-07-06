import uuid
from fastapi.testclient import TestClient
from services.profile.app.main import app, Base, engine, SessionLocal
from services.profile.app import models

Base.metadata.create_all(bind=engine)

client = TestClient(app)


def test_create_and_read_profile():
    db = SessionLocal()
    profile = models.Profile(user_id=uuid.uuid4(), first_name="John")
    db.add(profile)
    db.commit()
    user_id = profile.user_id
    db.close()

    response = client.get(f"/api/profile?user_id={user_id}")
    assert response.status_code == 200
    assert response.json()["user_id"] == str(user_id)


def test_experience_level_crud():
    response = client.post("/api/experience-levels", json={"label": "Junior", "sequence": 1})
    assert response.status_code == 200
    level_id = response.json()["id"]

    response = client.get("/api/experience-levels")
    assert response.status_code == 200
    assert len(response.json()) >= 1

    response = client.put(f"/api/experience-levels/{level_id}", json={"label": "Junior+", "sequence": 1})
    assert response.status_code == 200

    response = client.delete(f"/api/experience-levels/{level_id}")
    assert response.status_code == 200
