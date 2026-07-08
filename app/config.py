"""
app/config.py
─────────────
Central configuration loaded from environment variables.
All settings are accessed via the `settings` singleton.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GROQ_API_KEY: str   = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL:   str   = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    TEMPERATURE:  float = float(os.getenv("TEMPERATURE", "0"))
    MAX_ITERATIONS: int = int(os.getenv("MAX_ITERATIONS", "5"))
    MAX_QUESTION_LENGTH: int = 500

    def validate(self):
        if not self.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set. Please check your .env file.")


settings = Settings()