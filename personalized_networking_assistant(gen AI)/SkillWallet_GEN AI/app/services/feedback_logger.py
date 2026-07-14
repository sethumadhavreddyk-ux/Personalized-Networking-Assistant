
import json
from typing import List
from datetime import datetime

from config import get_settings


class FeedbackLogger:
    """Manages user feedback persistence."""

    def __init__(self, file_path=None):
        """Initialize the FeedbackLogger with a file path."""
        settings = get_settings()
        self.feedback_file = file_path or str(settings.FEEDBACK_FILE)

    def log_feedback(self, feedback_data: dict) -> None:
        """Append a feedback record to the feedback file."""
        feedback_list = self.get_feedback()
        feedback_data["logged_at"] = datetime.now().isoformat()
        feedback_list.append(feedback_data)
        with open(self.feedback_file, "w", encoding="utf-8") as f:
            json.dump(feedback_list, f, indent=2, ensure_ascii=False)

    def get_feedback(self) -> List[dict]:
        """Retrieve all feedback records."""
        try:
            with open(self.feedback_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def clear_feedback(self) -> None:
        """Clear all feedback records."""
        with open(self.feedback_file, "w", encoding="utf-8") as f:
            json.dump([], f)