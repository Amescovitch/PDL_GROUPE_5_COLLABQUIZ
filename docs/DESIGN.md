# DESIGN - CollabQuiz (draft)

## Architecture générale
- Backend: FastAPI + WebSocket (uvicorn)
- Frontend: Vue 3 + TypeScript + Pinia
- DB: PostgreSQL
- Auth: JWT

## Endpoints clés (exemples)
- POST /auth/register
- POST /auth/login
- GET /api/quizzes
- POST /api/quizzes
- GET /api/quizzes/{id}
- WebSocket: /ws/session/{sessionId}

## Data model (simplified)
- User, Quiz, Question, Choice, Attempt, Answer
