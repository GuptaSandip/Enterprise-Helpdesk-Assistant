"""
main.py
────────
Application entry point.
Initializes FastAPI, validates config, and registers all routes.
"""
"""
main.py
────────
Application entry point.
Initializes FastAPI, connects MongoDB on startup,
and registers all routes.

Serves FastAPI backend + React frontend (static files).
"""


from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from app.config import settings
from app.api.routes import router
from app.db.database import connect_db, disconnect_db
 
settings.validate()
 
 
@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await disconnect_db()
 
 
app = FastAPI(
    title="Enterprise Helpdesk Assistant",
    description="AI-powered enterprise helpdesk — Sandip Gupta",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)
 
# ── API routes ─────────────────────────────────────────────────────────────────
app.include_router(router)
 
# ── Serve React frontend (static build) ───────────────────────────────────────
static_dir = Path(__file__).parent / "static"
 
if static_dir.exists():
    app.mount("/assets", StaticFiles(directory=static_dir / "assets"), name="assets")
 
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve React app for all non-API routes."""
        return FileResponse(static_dir / "index.html")