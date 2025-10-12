import os
from dataclasses import dataclass


@dataclass
class Settings:
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "db")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "collabquiz")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "collabquiz")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "collabquiz")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))

    FRONTEND_ORIGIN: str = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        # If a consolidated DATABASE_URL is provided, use it.
        db_url = os.getenv("DATABASE_URL")
        if db_url:
            return db_url
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
