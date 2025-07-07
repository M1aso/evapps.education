# Project Setup Guide

This guide provides an overview of how to start building the platform described in `REQUIREMENTS.md`. The repository does not contain full source code; instead it gives a starting point for the architecture and configuration.

## 1. Repository Structure

```
README.md           - short project description
REQUIREMENTS.md     - functional and technical requirements
SETUP_GUIDE.md      - (this file) step-by-step setup instructions
.env.example        - example environment variable file
```

Services should be implemented under a top level `services/` directory. Each service may use its own language and framework as specified in the requirements. A sample implementation can be found at `services/notification`.

## 2. Prerequisites

- Docker and Docker Compose (or a local Kubernetes cluster such as `kind`)
- PostgreSQL client utilities
- Node.js and Python installed locally if you plan to run services without containers

## 3. Basic Steps

1. **Clone the repository**
   ```bash
   git clone <repo_url>
   cd evapps.education
   ```
2. **Create environment configuration**
   Copy the example file and fill in real credentials:
   ```bash
   cp .env.example .env
   ```
3. **Implement services**
   For each microservice listed in `REQUIREMENTS.md` create a subdirectory under `services/`. A minimal example could look like `services/auth/` with its own `Dockerfile` and application code. Use the variables from `.env` in your configuration.
4. **Run services locally**
   You can use Docker Compose or Kubernetes manifests. Ensure each service reads configuration from environment variables.

5. **Run tests**
   Example tests are provided for each service. From the repository root run:
   ```bash
   pytest services/auth/tests
   pytest services/profile/tests
   pytest services/analytics/tests
   pytest services/notification/tests
   ```
Go services have simple checks that can be executed with `go test`.
For Node-based services such as `services/chat` run `npm install` once to
download dependencies, then `npm test` inside the directory.

## 4. Environment Variables and Credentials

All sensitive credentials (database passwords, API tokens, secret keys) should be provided via environment variables. During local development they can be placed in the `.env` file which is loaded by Docker Compose or your application framework. For production, store them in Kubernetes Secrets or your CI/CD secret manager.

Below is a summary of typical variables for each service.

### Auth Service
- `AUTH_DATABASE_URL` – PostgreSQL connection string
- `JWT_SECRET` – secret key for signing JWT tokens
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD` – email sending credentials
- `SMS_API_TOKEN` – token for the SMS provider

### Profile Service
- `PROFILE_DATABASE_URL` – PostgreSQL connection string

### Content Service
- `CONTENT_DATABASE_URL` – PostgreSQL connection string
- `OBJECT_STORAGE_ENDPOINT` – URL of MinIO/Yandex Object Storage
- `OBJECT_STORAGE_BUCKET` – bucket name for course materials
- `OBJECT_STORAGE_ACCESS_KEY` and `OBJECT_STORAGE_SECRET_KEY` – credentials for object storage

### Notification Service
- `REDIS_URL` – Redis connection string for Celery
- `RABBITMQ_URL` – RabbitMQ connection string
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD` – email gateway credentials
- `TELEGRAM_BOT_TOKEN` – Telegram bot API token

### Chat Service
- `CHAT_DATABASE_URL` – PostgreSQL connection string
- `CHAT_REDIS_URL` – Redis connection for WebSocket sessions

### Analytics Service
- `ANALYTICS_DATABASE_URL` – PostgreSQL connection string
- `RABBITMQ_URL` – queue broker for report generation tasks

### Other Common Variables
- `LOG_LEVEL` – application log level
- `PORT` – service listening port

Environment variables can be adjusted for each deployment environment (dev/staging/prod). When deploying to Kubernetes, define these variables inside `Deployment` manifests or Helm charts using `env` and `envFrom` sections to pull from ConfigMaps/Secrets.

## 5. Next Steps

The repository currently only contains documentation. Start by creating the service folders and gradually implement the APIs as defined in `REQUIREMENTS.md`. Each service should have its own tests and CI/CD pipeline.

## 6. Running with Docker Compose

For local development you can spin up the services using Docker Compose. The
repository does not include a Compose file, but a simple example would look like

```yaml
version: '3.9'
services:
  auth:
    build: ./services/auth
    env_file: .env
  profile:
    build: ./services/profile
    env_file: .env
```

After creating such a file, run:

```bash
docker compose up --build
```

Each service exposes its API on the port defined by the `PORT` environment
variable.


## 7. Gateway and Logging

The platform routes requests through an API gateway. See the [API Gateway section](README.md#api-gateway) in the README along with the sample configuration in [`docker/nginx/app.conf`](docker/nginx/app.conf). For log viewing instructions refer to [Centralized Logging with EFK](README.md#centralized-logging-with-efk).
