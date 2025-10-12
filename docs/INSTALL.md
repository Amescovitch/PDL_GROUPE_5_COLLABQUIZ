# INSTALL - CollabQuiz (Starter)

## Prérequis
- Docker & Docker Compose
- git
- (optionnel) Python 3.12 local for tests

## Lancer le projet
1. Copier l'exemple d'env:
    - Unix / macOS:
       ```bash
       cp .env.example .env
       ```
    - PowerShell (Windows):
       ```powershell
       Copy-Item .env.example .env
       ```

    Note: `.env.example` contient à la fois les variables `POSTGRES_*` et une variable consolidée `DATABASE_URL`.
    Si `DATABASE_URL` est définie, elle sera utilisée par SQLAlchemy/Alembic. Exemple:
    ```text
    DATABASE_URL=postgresql+psycopg2://collabquiz:collabquiz@db:5432/collabquiz
    ```
2. Construire et démarrer:
   ```bash
   docker-compose up --build
   ```

## Backend
- API: http://localhost:8000
- Docs OpenAPI: http://localhost:8000/docs

## Tests
- Backend (dans le conteneur ou local): `pytest`
- Frontend: `npm run test` (vitest) / `npm run e2e` (cypress) when configured

## Migrations Alembic (initialisation)

Si tu veux initialiser les migrations localement:

```bash
cd backend
# créer l'environnement alembic si non présent
alembic init alembic
# modifier alembic.ini/env.py pour utiliser DATABASE_URL (déjà scaffoldé dans le repo)
alembic revision --autogenerate -m "init"
alembic upgrade head
```

