import os
from dataclasses import dataclass
from dotenv import load_dotenv
from pathlib import Path

# On charge le .env depuis la racine du projet
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # remonte de /backend/app jusqu'à la racine
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    print(f" Fichier .env non trouvé à {env_path}")

@dataclass
class Settings:

    # Détection automatique : local ou Docker
    IS_RUNNING_LOCAL: bool = os.getenv("RUNNING_LOCAL", "false").lower() == "true"

    # Database
    POSTGRES_HOST: str = (
        "localhost" if IS_RUNNING_LOCAL else os.getenv("POSTGRES_HOST", "db")
    )
    """
    Configuration principale de l’application CollabQuiz.
    Charge les variables d’environnement (Docker ou .env local).
    """

    # --- Configuration base de données PostgreSQL ---
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "db")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "collabquiz")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "collabquiz")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "collabquiz")

    # --- Clé secrète et sécurité ---
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    # --- Configuration serveur FastAPI ---
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    # --- CORS et frontend ---
    FRONTEND_ORIGIN: str = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

    # --- URL complète de la base SQLAlchemy ---
    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        """
        Retourne l’URL de connexion PostgreSQL complète pour SQLAlchemy.
        Si DATABASE_URL est défini, il est prioritaire (utile pour Render/Heroku).
        """
        db_url = os.getenv("DATABASE_URL")
        if db_url:
            # Si une URL complète est fournie (ex: Render, Railway, etc.)
            if db_url.startswith("postgres://"):
                db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
            return db_url

        # Sinon, construire l’URL à partir des variables individuelles
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


# Instance globale utilisée dans tout le projet
settings = Settings()
