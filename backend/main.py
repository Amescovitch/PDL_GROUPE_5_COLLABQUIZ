from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

# Support importing config both as package (backend.config) and as module (config)
try:
    from backend.config import settings  # type: ignore
except Exception:
    from app.config import settings

app = FastAPI(title="CollabQuiz API")

# CORS (autoriser le frontend local)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    """Endpoint pour vérifier que le service tourne"""
    return {"status": "ok"}


@app.websocket("/ws/session/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """Simple WebSocket stub pour le mode live.
    Accepte la connexion et renvoie un message de bienvenue.
    """
    await websocket.accept()
    await websocket.send_json({"message": f"connected to session {session_id}"})
    try:
        while True:
            data = await websocket.receive_text()
            # echo for now
            await websocket.send_text(f"echo: {data}")
    except Exception:
        await websocket.close()


