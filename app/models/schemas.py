"""
app/models/schemas.py
──────────────────────
Pydantic models for request validation and response serialization.
Includes guardrails: empty check, length limit, injection detection.
"""

from typing import Optional
from pydantic import BaseModel, field_validator
from app.config import settings


BLOCKED_PATTERNS = [
    "drop table", "delete from",
    "ignore previous instructions",
    "ignore all instructions",
    "you are now",
]


class AskRequest(BaseModel):
    question:   str
    session_id: Optional[str] = "default"

    @field_validator("question")
    @classmethod
    def validate_question(cls, v: str) -> str:
        v = v.strip()

        if not v:
            raise ValueError("Question cannot be empty.")

        if len(v) > settings.MAX_QUESTION_LENGTH:
            raise ValueError(
                f"Question too long. Maximum {settings.MAX_QUESTION_LENGTH} characters allowed."
            )

        if any(pattern in v.lower() for pattern in BLOCKED_PATTERNS):
            raise ValueError("Invalid input detected. Please ask a valid business question.")

        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "question": "Create a high priority ticket — WiFi is down on floor 2",
                "session_id": "user-session-001",
            }
        }
    }


class AskResponse(BaseModel):
    question:   str
    answer:     str
    session_id: str
    status:     str    # success | fallback | error

    model_config = {
        "json_schema_extra": {
            "example": {
                "question": "Create a high priority ticket — WiFi is down on floor 2",
                "answer":   "Ticket Created\n  ID: TKT-A1B2C3D4 ...",
                "session_id": "user-session-001",
                "status":   "success",
            }
        }
    }


class HealthResponse(BaseModel):
    status:    str
    service:   str
    version:   str
    timestamp: str


class TicketsResponse(BaseModel):
    total:   int
    tickets: list