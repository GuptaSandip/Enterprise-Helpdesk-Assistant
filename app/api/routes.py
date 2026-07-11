"""
app/api/routes.py
──────────────────
All FastAPI route definitions.

Endpoints:
  POST   /ask              → main AI assistant
  GET    /tickets          → view all tickets from MongoDB
  GET    /health           → health check
  DELETE /session/{id}     → clear conversation memory
  GET    /sessions         → list active sessions
"""

from datetime import datetime
from fastapi import APIRouter, HTTPException

from app.models.schemas import AskRequest, AskResponse, HealthResponse, TicketsResponse
from app.agent.agent import agent_with_memory, llm_fallback
from app.db.database import get_db
from app.memory.session import clear_session, get_active_sessions

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["System"])
async def health():
    """Returns service health status."""
    return HealthResponse(
        status="healthy",
        service="Enterprise Helpdesk Assistant",
        version="2.0.0",
        timestamp=datetime.utcnow().isoformat(),
    )


@router.get("/tickets", response_model=TicketsResponse, tags=["Tickets"])
async def get_all_tickets():
    """Fetch all tickets from MongoDB."""
    db      = await get_db()
    cursor  = db.tickets.find({}, {"_id": 0})
    tickets = await cursor.to_list(length=1000)
    return TicketsResponse(total=len(tickets), tickets=tickets)


@router.delete("/session/{session_id}", tags=["Memory"])
async def delete_session(session_id: str):
    """Clear conversation memory for a specific session."""
    deleted = clear_session(session_id)
    if deleted:
        return {"message": f"Session '{session_id}' cleared successfully."}
    return {"message": f"No active session found with ID '{session_id}'."}


@router.get("/sessions", tags=["Memory"])
async def list_sessions():
    """List all currently active session IDs."""
    sessions = get_active_sessions()
    return {"active_sessions": sessions, "count": len(sessions)}


@router.post("/ask", response_model=AskResponse, tags=["Assistant"])
async def ask(request: AskRequest):
    """
    Core AI assistant endpoint.

    Engineering improvements:
      1. Tool Calling       — Agent selects the right MongoDB-backed business action
      2. Conversation Memory — Per-session history for multi-turn dialogue
      3. Fallback Logic      — Direct LLM call if agent pipeline fails
      4. Input Guardrails    — Pydantic validation + injection detection
    """
    config = {"configurable": {"session_id": request.session_id}}

    # ── Primary: Agent with tool calling + memory ──
    try:
        result = await agent_with_memory.ainvoke(
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
        print(f"[WARN] Agent failed: {agent_error}. Activating fallback...")

        # ── Fallback: Direct LLM call ──
        try:
            fallback_answer = llm_fallback(request.question)
            return AskResponse(
                question=request.question,
                answer=f"[Fallback Response]\n{fallback_answer}",
                session_id=request.session_id,
                status="fallback",
            )
        except Exception as fallback_error:
            print(f"[ERROR] Fallback failed: {fallback_error}")
            raise HTTPException(
                status_code=503,
                detail="Service temporarily unavailable. Please try again shortly.",
            )