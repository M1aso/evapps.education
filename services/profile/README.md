# Profile Service

This is a minimal implementation of the Profile and Social Accounts module described in `REQUIREMENTS.md`.

The service uses **FastAPI** and **SQLAlchemy**. The default database is SQLite for local development, but `PROFILE_DATABASE_URL` can point to PostgreSQL in production.

## Endpoints

- `GET /api/profile?user_id=` — retrieve profile and linked social accounts
- `PUT /api/profile?user_id=` — update profile fields
- `POST /api/profile/avatar?user_id=` — upload avatar image (≤5MB)
- `GET/POST/PUT/DELETE /api/experience-levels` — CRUD operations for experience levels
- `POST /api/profile/social/link` — link a social account
- `DELETE /api/profile/social/{provider}?user_id=` — unlink
- `GET /api/profile/history?user_id=&page=&per_page=` — change history

Launch locally with:

```bash
uvicorn app.main:app --reload
```

## Running Tests

Use `pytest` from the repository root:

```bash
pytest services/profile/tests
```

