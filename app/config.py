"""
app/config.py
─────────────
Central configuration loaded from environment variables.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Groq
    GROQ_API_KEY:    str   = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL:      str   = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    TEMPERATURE:     float = float(os.getenv("TEMPERATURE", "0"))
    MAX_ITERATIONS:  int   = int(os.getenv("MAX_ITERATIONS", "5"))

    # MongoDB
    MONGODB_URI:     str   = os.getenv("MONGODB_URI", "")
    MONGODB_DB_NAME: str   = os.getenv("MONGODB_DB_NAME", "enterprise_assistant_db")

    # LangSmith
    LANGCHAIN_API_KEY:      str = os.getenv("LANGCHAIN_API_KEY", "")
    LANGCHAIN_PROJECT:      str = os.getenv("LANGCHAIN_PROJECT", "FluidAI-Enterprise-Assistant")

    # Validation
    MAX_QUESTION_LENGTH: int = 500

    def validate(self):
        if not self.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set.")
        if not self.MONGODB_URI:
            raise ValueError("MONGODB_URI is not set.")
        if not self.LANGCHAIN_API_KEY:
            print("[WARN] LANGCHAIN_API_KEY not set — LangSmith tracing disabled.")


settings = Settings()