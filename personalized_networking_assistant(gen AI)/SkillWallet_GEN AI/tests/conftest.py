
import pytest
import tempfile
import shutil
from pathlib import Path
from fastapi.testclient import TestClient

from main import app
from app.routers.conversation import (
    get_event_analyzer,
    get_topic_generator,
    get_fact_checker,
    get_history_logger,
    get_feedback_logger,
)
from app.services.event_analyzer import EventAnalyzer
from app.services.topic_generator import TopicGenerator
from app.services.fact_checker import FactChecker
from app.services.history_logger import HistoryLogger
from app.services.feedback_logger import FeedbackLogger
class MockEventAnalyzer:
    def analyze_event(self, event_name: str, user_role: str) -> dict:
        return {
            "event_name": event_name,
            "user_role": user_role,
            "themes": [{"theme": "Technology", "confidence": 0.95}],
            "audience_profile": "Technical professionals focused on implementation and architecture"
        }

    def extract_themes(self, event_name: str) -> list:
        return [{"theme": "Technology", "confidence": 0.95}]


class MockTopicGenerator:
    def generate_topics(self, event_context: dict, user_interests: list) -> list:
        return [
            {
                "topic": "Technology in Networking Event",
                "talking_points": [
                    {"point": "Key Trends", "details": "Discuss emerging trends in Technology."}
                ]
            }
        ]

    def generate_talking_points(self, topic: str, event_context: dict = None) -> list:
        return [{"point": "Key Trends", "details": f"Discuss emerging trends in {topic}."}]


class MockFactChecker:
    def check_facts(self, topics: list) -> list:
        return [self.verify_claim(t) for t in topics]

    def verify_claim(self, claim: str) -> dict:
        return {
            "claim": claim,
            "verified": True,
            "confidence": 0.85,
            "source": "https://en.wikipedia.org/wiki/Technology",
            "summary": "Mock technology description from wikipedia."
        }

@pytest.fixture(scope="session", autouse=True)
def mock_dependencies():
    """Override expensive model dependencies globally for testing."""
    app.dependency_overrides[get_event_analyzer] = lambda: MockEventAnalyzer()
    app.dependency_overrides[get_topic_generator] = lambda: MockTopicGenerator()
    app.dependency_overrides[get_fact_checker] = lambda: MockFactChecker()
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def test_client(tmp_path):
    """Create a FastAPI TestClient instance with localized logger files."""
    # Create temp files for history and feedback logging
    temp_history = tmp_path / "history.json"
    temp_feedback = tmp_path / "feedback.json"
    temp_history.write_text("[]", encoding="utf-8")
    temp_feedback.write_text("[]", encoding="utf-8")

    # Override logger dependencies to use temp files
    mock_history_logger = HistoryLogger(file_path=str(temp_history))
    mock_feedback_logger = FeedbackLogger(file_path=str(temp_feedback))

    app.dependency_overrides[get_history_logger] = lambda: mock_history_logger
    app.dependency_overrides[get_feedback_logger] = lambda: mock_feedback_logger

    with TestClient(app) as client:
        yield client


@pytest.fixture
def sample_conversation_request():
    """Return a sample ConversationRequest payload."""
    return {
        "event_name": "Tech Summit 2026",
        "user_role": "Developer",
        "user_interests": ["AI", "Cloud", "Python"]
    }


@pytest.fixture
def sample_feedback_request():
    """Return a sample FeedbackRequest payload."""
    return {
        "conversation_id": "test-session-uuid-12345",
        "rating": 5,
        "comments": "Excellent custom talking points!"
    }


@pytest.fixture
def sample_event_context():
    """Return a sample event context dictionary."""
    return {
        "event_name": "Tech Summit 2026",
        "user_role": "Developer",
        "themes": [{"theme": "Technology", "confidence": 0.95}],
        "audience_profile": "Technical professionals focused on implementation and architecture"
    }