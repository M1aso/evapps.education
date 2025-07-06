# Analytics Service

This service implements the Analytics and Reporting module described in `REQUIREMENTS.md`.
It exposes REST API endpoints using FastAPI and processes report generation tasks
via Celery workers. Reports can be generated in PDF or XLSX format.

## Features

- Dashboard metrics endpoint (`/api/analytics/dashboard`).
- CRUD for report requests and schedules.
- Asynchronous generation of PDF/XLSX reports.
- PostgreSQL as the primary datastore.
- Celery with RabbitMQ for background tasks.

## Development

### Prerequisites
- Python 3.10+
- PostgreSQL instance
- RabbitMQ instance

### Setup
```bash
cd services/analytics
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp ../../.env.example .env  # adjust variables
```

### Running API
```bash
uvicorn app.main:app --reload
```

### Running Celery worker
```bash
celery -A app.tasks worker -B --loglevel=info
```

`-B` enables the beat scheduler for scheduled reports.

## Docker
A sample `Dockerfile` is provided. Build and run using your preferred container
tools.
