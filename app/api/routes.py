"""
app/api/routes.py
──────────────────
All FastAPI route definitions.
Keeps route logic separate from app initialization (main.py).

Endpoints:
  POST   /ask                → main AI assistant
  GET    /tickets            → view all tickets
  GET    /health             → health check
  DELETE /session/{id}       → clear conversation memory
"""

from datetime import datetime
from fastapi import APIRouter, HTTPException

from app.models.schemas import AskRequest, AskResponse, HealthResponse, TicketsResponse
from app.agent.agent import agent_with_memory, llm_fallback
from app.db.mock_db import tickets_db
from app.memory.session import clear_session, get_active_sessions

router = APIRouter()


# ── Health check ───────────────────────────────────────────────────────────────

@router.get("/health", response_model=HealthResponse, tags=["System"])
async def health():
    """Returns service health status and metadata."""
    return HealthResponse(
        status="healthy",
        service="Fluid AI – Enterprise Assistant",
        version="2.0.0",
        timestamp=datetime.now().isoformat(),
    )


# ── Ticket viewer ──────────────────────────────────────────────────────────────

@router.get("/tickets", response_model=TicketsResponse, tags=["Tickets"])
async def get_all_tickets():
    """View all tickets currently in the mock database."""
    return TicketsResponse(
        total=len(tickets_db),
        tickets=list(tickets_db.values()),
    )


# ── Session management ─────────────────────────────────────────────────────────

@router.delete("/session/{session_id}", tags=["Memory"])
async def delete_session(session_id: str):
    """
    Clear conversation memory for a specific session.
    Useful for starting a fresh conversation context.
    """
    deleted = clear_session(session_id)
    if deleted:
        return {"message": f"Session '{session_id}' cleared successfully."}
    return {"message": f"No active session found with ID '{session_id}'."}


@router.get("/sessions", tags=["Memory"])
async def list_sessions():
    """List all currently active session IDs (for debugging)."""
    sessions = get_active_sessions()
    return {"active_sessions": sessions, "count": len(sessions)}


# ── Core AI endpoint ───────────────────────────────────────────────────────────

@router.post("/ask", response_model=AskResponse, tags=["Assistant"])
async def ask(request: AskRequest):
    """
    Core AI assistant endpoint.

    Processes a business question through a LangChain tool-calling agent
    with per-session conversation memory.

    Engineering improvements implemented:
      1. Tool Calling       — Agent selects the right business action tool automatically
      2. Conversation Memory — Per-session history enables natural multi-turn dialogue
      3. Fallback Logic      — Direct LLM call if agent pipeline fails
      4. Input Guardrails    — Pydantic validation: empty check, length limit, injection detection
    """
    config = {"configurable": {"session_id": request.session_id}}

    # ── Primary path: Agent with tool calling + conversation memory ──
    try:
        result = agent_with_memory.invoke(
            {"input": request.question},
            config=config,
        )
        return AskResponse(
            question=request.question,
            answer=result["output"],
            session_id=request.session_id,
            status="success",
        )

    except Exception as agent_error:
        print(f"[WARN] Agent pipeline failed: {agent_error}. Activating fallback...")

        # ── Fallback path: Direct LLM call ──
        try:
            fallback_answer = llm_fallback(request.question)
            return AskResponse(
                question=request.question,
                answer=f"[Fallback Response]\n{fallback_answer}",
                session_id=request.session_id,
                status="fallback",
            )

        except Exception as fallback_error:
            print(f"[ERROR] Fallback also failed: {fallback_error}")
            raise HTTPException(
                status_code=503,
                detail="Service temporarily unavailable. Please try again shortly.",
            )