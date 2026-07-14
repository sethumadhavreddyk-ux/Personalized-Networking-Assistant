
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Settings:
    """Central configuration settings for the application."""

    # Project metadata
    PROJECT_NAME: str = "SkillWallet GenAI — Personalized Networking Assistant"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = (
        "AI-powered assistant that generates personalized conversation "
        "topics for professional networking events using DistilBERT "
        "and GPT-2."
    )

    # Server settings
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))

    # ── Model Settings ───────────────────────
    DISTILBERT_MODEL: str = "distilbert-base-uncased"
    GPT2_MODEL: str = "gpt2"

    # GPT-2 generation parameters
    MAX_NEW_TOKENS: int = 150
    TEMPERATURE: float = 0.8
    TOP_K: int = 50
    TOP_P: float = 0.9

    # ── File Paths ───────────────────────────
    HISTORY_FILE: Path = BASE_DIR / "history.json"
    FEEDBACK_FILE: Path = BASE_DIR / "feedback.json"

    # ── CORS ─────────────────────────────────
    CORS_ORIGINS: list = ["*"]

    # ── Candidate Themes for Classification ──
    CANDIDATE_THEMES: list = [
        "Technology",
        "Business",
        "Healthcare",
        "Finance",
        "Education",
        "Marketing",
        "Engineering",
        "Science",
        "Artificial Intelligence",
        "Data Science",
        "Cybersecurity",
        "Cloud Computing",
        "Sustainability",
        "Leadership",
        "Entrepreneurship",
        "Innovation",
        "Networking",
        "Career Development",
        "Digital Transformation",
        "Product Management",
        "Software Development",
        "Design",
    ]

def get_settings() -> Settings:
    return Settings()