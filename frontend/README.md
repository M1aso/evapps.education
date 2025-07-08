# Frontend

This directory contains the web application for the learning platform. It is currently a placeholder but follows a typical Node.js/React layout.

## Getting Started

1. **Install dependencies**
   ```bash
   npm install
   ```
2. **Create environment file**
   Copy `.env.example` to `.env.local` and update the variables:
   ```bash
   cp .env.example .env.local
   ```
3. **Run the development server**
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:3000` by default.

## Project Structure

```
frontend/
├── components/    # Reusable React components
├── pages/         # Application pages/routes
├── public/        # Static assets
└── tests/         # Unit and integration tests
```

## Key Commands

| Command           | Description                   |
|------------------ |------------------------------ |
| `npm run lint`    | Run ESLint to check code style |
| `npm test`        | Execute test suite            |
| `npm run build`   | Create a production build     |

