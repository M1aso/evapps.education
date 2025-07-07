# Notification Service

This is a basic skeleton implementation for the Notification Service described in `REQUIREMENTS.md`.
It provides REST endpoints for managing notification templates, user settings, and a queue for
sending messages via email and Telegram. The service uses FastAPI and SQLAlchemy and is intended
as a starting point for further development.

## Features

- CRUD for notification templates (admin only)
- User notification settings (enable/disable channels)
- Queue management API for background delivery via Celery
- Example Celery tasks for sending emails or Telegram messages

The service relies on PostgreSQL for persistent storage and RabbitMQ/Redis for the task queue.
Environment variables are loaded from the surrounding project `.env` file.
Ensure that `NOTIFICATION_DATABASE_URL` uses the `asyncpg` driver, e.g.
`postgresql+asyncpg://user:password@localhost:5432/notification_db`, so that the
async SQLAlchemy engine can connect without requiring the `psycopg2` package.
