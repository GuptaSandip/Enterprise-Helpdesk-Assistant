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
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.api.routes import router
from app.db.database import connect_db, disconnect_db

# Validate env on startup
settings.validate()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage MongoDB connection lifecycle."""
    await connect_db()
    yield
    await disconnect_db()


app = FastAPI(
    title="Enterprise Helpdesk Assistant",
    description=(
        "AI-powered enterprise helpdesk with tool calling, "
        "conversation memory, MongoDB persistence, and fallback logic.\n\n"
        "**Author:** Sandip Gupta | AI Engineer & Master Trainer"
    ),
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(router)