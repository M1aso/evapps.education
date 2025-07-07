# Content Service

This is a minimal placeholder implementation of the Content Management Module described in `REQUIREMENTS.md`.
It provides simple in-memory CRUD endpoints for courses, sections and materials.

The service is intentionally lightweight and does not include persistent storage or video processing.
It demonstrates the basic API structure so other services can integrate during early development.

## Running

```bash
cd services/content
go run .
```

The service listens on port `8000` and exposes JSON endpoints under `/api`.
Swagger UI for exploring the API is served at `http://localhost:8000/docs` or
via the gateway at `http://localhost:8080/content/docs`.
