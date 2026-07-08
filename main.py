"""
main.py
────────
Application entry point.
Initializes FastAPI, validates config, and registers all routes.
"""

from fastapi import FastAPI
from app.config import settings
from app.api.routes import router

# Validate environment on startup
settings.validate()

app = FastAPI(
    title="Fluid AI – Enterprise Assistant",
    description=(
        "AI-powered enterprise helpdesk with tool calling, "
        "conversation memory, fallback logic, and request guardrails.\n\n"
        "**Author:** Sandip Gupta | AI Solutions Engineer Challenge"
    ),
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(router)