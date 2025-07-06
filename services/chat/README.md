# Chat Service

This directory contains a minimal implementation of the Chat Service described in
[`REQUIREMENTS.md`](../../REQUIREMENTS.md). It uses Express for the REST API,
`ws` for WebSocket connections and Sequelize with SQLite for persistence. The
service is intentionally lightweight and meant for local experimentation.

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```
If you start the service without running this command you will see the
message `sequelize not installed, using stub models` and the server will fail
to initialize.
When using Docker Compose make sure to run
`docker compose up --build` so the image installs all dependencies during the
build step.
2. Start the server:
   ```bash
   npm start
   ```
   The service listens on the port defined in the `PORT` environment variable (default `3000`).

WebSocket connections should use the path `/ws/chats/:chatId`.

## API Documentation

When running in development you can view Swagger UI at `http://localhost:3000/docs`.
