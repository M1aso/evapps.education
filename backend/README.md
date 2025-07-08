# evapps.education

This repository contains documentation and helper files for a corporate e‑learning platform.

- The high level requirements are described in [REQUIREMENTS.md](REQUIREMENTS.md).
- Follow [SETUP_GUIDE.md](SETUP_GUIDE.md) for local development steps and environment variable configuration.

This code base provides a minimal working skeleton. Each microservice lives under
`services/` and includes its own dependencies and example tests. Use the
documentation in this repository to continue building out the platform.

## Implemented Services

- **Auth service** – `services/auth` (Python/FastAPI) with unit tests in
  `services/auth/tests`.
- **Profile service** – `services/profile` (Python/FastAPI) with unit tests in
  `services/profile/tests`.
- **Content service** – `services/content` (Go) providing a simple in-memory
  API. Tests can be executed with `go test`.
- **Chat service** – `services/chat` (Node.js/Express) exposing REST and
  WebSocket endpoints. Run `npm install` once to fetch dependencies, then
  `npm test` inside the directory to run a basic check.
- **Notification service** – `services/notification` (Python/FastAPI + Celery)
  with example tests in `services/notification/tests`.
- **Analytics service** – `services/analytics` (Python/FastAPI + Celery) with
  example tests in `services/analytics/tests`.

## API Gateway

The architecture routes all incoming traffic through an API gateway. As noted in
`REQUIREMENTS.md` line 21, this gateway validates JWT tokens, terminates TLS and
forwards requests to the microservices. A minimal Nginx example is provided in
[`docker/nginx/app.conf`](docker/nginx/app.conf). The default
`docker-compose.yml` starts a `gateway` service using this file so the platform
is reachable at `http://localhost:8080`.

### Accessing Services via the Gateway

After running `docker compose up --build` you can browse each module through
Nginx using the following paths:

| Service         | Endpoint                               |
|-----------------|-----------------------------------------|
| Auth            | `http://localhost:8080/auth/docs`       |
| Profile         | `http://localhost:8080/profile/docs`    |
| Content         | `http://localhost:8080/content/docs`    |
| Chat            | `http://localhost:8080/chat/docs`       |
| Notification    | `http://localhost:8080/notification/docs` |
| Analytics       | `http://localhost:8080/analytics/docs`  |

Each service exposes its own Swagger UI under `/docs` for interactive API
testing. Replace `/docs` with other paths as appropriate for your implementation.

### Troubleshooting 502 Errors

If the gateway returns a **502 Bad Gateway** when opening one of the service
documentation pages (e.g. `/notification/docs`), the underlying container likely
failed to start or is still initializing. Run `docker compose ps` and
`docker compose logs <service>` to inspect errors. Database connections are a
common cause—ensure Postgres is reachable and environment variables are set
correctly, then restart the affected container.

## Centralized Logging with EFK

Lines 31 and 532 of `REQUIREMENTS.md` specify the use of an EFK (Elasticsearch,
Fluentd, Kibana) stack for aggregating service logs. Deploy Elasticsearch and
Fluentd, expose Kibana (for example on port 5601) and configure Fluentd to
forward container output. Once deployed, open Kibana to search and visualize
logs from every service.
