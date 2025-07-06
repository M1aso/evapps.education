# evapps.education

This repository contains documentation and helper files for a corporate e‑learning platform.

- The high level requirements are described in [REQUIREMENTS.md](REQUIREMENTS.md).
- Follow [SETUP_GUIDE.md](SETUP_GUIDE.md) for local development steps and environment variable configuration.

This code base is only a skeleton to help you start building the services described in the requirements document.

## Implemented Services

- `services/analytics` – initial implementation of the Analytics and Reporting module. It exposes FastAPI endpoints and Celery tasks for report generation.
- `services/notification` – example Notification Service implementation found under `services/notification`.
