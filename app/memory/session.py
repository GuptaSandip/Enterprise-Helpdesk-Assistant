"""
app/memory/session.py
──────────────────────
Per-session conversation memory using LangChain's ChatMessageHistory.

Each session_id gets its own isolated chat history, enabling
multi-turn conversations without context leaking between users.

Note: In production, replace the in-memory dict with Redis
      for persistence and horizontal scalability.
"""

from langchain_community.chat_message_histories import ChatMessageHistory

# In-memory session store: { session_id → ChatMessageHistory }
_session_store: dict[str, ChatMessageHistory] = {}


def get_session_history(session_id: str) -> ChatMessageHistory:
    """
    Retrieve or create a ChatMessageHistory for the given session ID.
    Creates a new empty history if the session doesn't exist yet.
    """
    if session_id not in _session_store:
        _session_store[session_id] = ChatMessageHistory()
    return _session_store[session_id]


def clear_session(session_id: str) -> bool:
    """
    Delete the conversation history for a given session.
    Returns True if session existed and was deleted, False otherwise.
    """
    if session_id in _session_store:
        del _session_store[session_id]
        return True
    return False


def get_active_sessions() -> list[str]:
    """Return a list of all active session IDs."""
    return list(_session_store.keys())