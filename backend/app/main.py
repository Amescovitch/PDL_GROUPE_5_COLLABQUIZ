from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Import propre de la configuration
from app.config import settings
from app.database import Base, engine
import app.models  # important : pour que Base.metadata connaisse toutes les tables

# Lancement / arrêt (future-proof)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ici, on peut initialiser la base de données ou d'autres services au démarrage
    print("Application CollabQuiz démarrée...")
    yield
    print("Application CollabQuiz arrêtée.")

# Initialisation de l’application FastAPI
app = FastAPI(title="CollabQuiz API", lifespan=lifespan)

# Middleware CORS pour autoriser le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Endpoints basiques ---
@app.get("/health")
async def health():
    """Vérifie que le service tourne correctement."""
    return {"status": "ok"}

# --- WebSocket de test (future live session) ---
@app.websocket("/ws/session/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """Simple WebSocket de démo pour les sessions live."""
    await websocket.accept()
    await websocket.send_json({"message": f"connected to session {session_id}"})
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"echo: {data}")
    except Exception:
        await websocket.close()
