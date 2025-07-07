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

## Centralized Logging with EFK

Lines 31 and 532 of `REQUIREMENTS.md` specify the use of an EFK (Elasticsearch,
Fluentd, Kibana) stack for aggregating service logs. Deploy Elasticsearch and
Fluentd, expose Kibana (for example on port 5601) and configure Fluentd to
forward container output. Once deployed, open Kibana to search and visualize
logs from every service.
