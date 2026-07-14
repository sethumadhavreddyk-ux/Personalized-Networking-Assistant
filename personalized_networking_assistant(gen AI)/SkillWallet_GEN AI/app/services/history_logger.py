"""
history_logger.py

Service for storing and retrieving conversation history.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List

from config import get_settings


class HistoryLogger:
    """Handles conversation history stored in history.json."""

    def __init__(self):
        settings = get_settings()
        self.history_file = Path(settings.HISTORY_FILE)

        # Create file if it doesn't exist
        if not self.history_file.exists():
            self.history_file.write_text("[]", encoding="utf-8")

    def get_history(self) -> List[dict]:
        """Return all stored conversations."""
        try:
            with open(self.history_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def log_conversation(self, conversation_data: dict) -> None:
        """Save a new conversation."""
        history = self.get_history()

        conversation_data["logged_at"] = datetime.now().isoformat()

        history.append(conversation_data)

        with open(self.history_file, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=4, ensure_ascii=False)

    def clear_history(self) -> None:
        """Delete all conversation history."""
        with open(self.history_file, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)