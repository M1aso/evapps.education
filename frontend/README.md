# Frontend

This is the Next.js web application for the education platform.

## Getting Started

1. Copy the environment variables and update them if needed:

```bash
cp env.example .env.local
```

2. Install dependencies and run the development server:

```bash
npm install
npm run dev
```

The app will be available at <http://localhost:3000>.

## Running with the Backend

Start the backend using Docker Compose from the repository root:

```bash
docker compose up
```

Then in this `frontend` folder run `npm install` followed by `npm run dev`.
