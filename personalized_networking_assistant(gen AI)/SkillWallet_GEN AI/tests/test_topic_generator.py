
import pytest
from unittest.mock import MagicMock
from app.services.topic_generator import TopicGenerator

def test_generate_topics_returns_list():
    """Test that generate_topics returns a list."""
    generator = TopicGenerator.__new__(TopicGenerator)
    generator.generate_talking_points = MagicMock(return_value=[
        {"point": "Key Trends", "details": "Discuss emerging trends."}
    ])
    event_context = {
        "event_name": "Tech Summit",
        "themes": [{"theme": "Technology", "confidence": 0.95}]
    }

    result = generator.generate_topics(event_context, ["AI"])
    assert isinstance(result, list)
    assert len(result) > 0
    assert result[0]["topic"] == "Technology in Tech Summit"


def test_generate_topics_non_empty():
    """Test that generated topics list is not empty."""
    generator = TopicGenerator.__new__(TopicGenerator)
    generator.generate_talking_points = MagicMock(return_value=[
        {"point": "Key Trends", "details": "Discuss emerging trends."}
    ])
    event_context = {
        "event_name": "Tech Summit",
        "themes": []
    }

    # Fallback path (combined list is empty, should append fallback topic)
    generator._fallback_points = MagicMock(return_value=[
        {"point": "Trends", "details": "Detailed trends"}
    ])
    result = generator.generate_topics(event_context, [])
    assert len(result) > 0
    assert "General Networking" in result[0]["topic"]
def test_generate_talking_points_returns_list():
    """Test that generate_talking_points returns a list."""
    generator = TopicGenerator.__new__(TopicGenerator)
    generator.generator = MagicMock(return_value=[
        {"generated_text": "Professional networking conversation about AI at Tech Summit.\nKey discussion points:\n1. Cloud architectures are evolving.\n2. Scale is critical."}
    ])
    generator.max_new_tokens = 128
    generator.temperature = 0.7
    generator.top_k = 50
    generator.top_p = 0.9
    generator._build_prompt = MagicMock(return_value="Prompt template")
    generator._parse_talking_points = MagicMock(return_value=[
        {"point": "Point A", "details": "Details A"}
    ])

    result = generator.generate_talking_points("AI", {"event_name": "Tech Summit"})
    assert isinstance(result, list)
    assert len(result) == 1


def test_generate_talking_points_non_empty():
    """Test that talking points list is not empty by falling back."""
    generator = TopicGenerator.__new__(TopicGenerator)
    generator.generator = MagicMock(side_effect=RuntimeError("Model error"))
    generator.max_new_tokens = 128
    generator.temperature = 0.7
    generator.top_k = 50
    generator.top_p = 0.9
    generator._build_prompt = MagicMock(return_value="Prompt template")

    result = generator.generate_talking_points("AI", {"event_name": "Tech Summit"})
    assert isinstance(result, list)
    assert len(result) > 0
    assert "point" in result[0]
    assert "details" in result[0]

def test_build_prompt_returns_string():
    """Test that _build_prompt returns a string."""
    generator = TopicGenerator.__new__(TopicGenerator)
    prompt = generator._build_prompt("AI", {"event_name": "Tech Summit"})
    assert isinstance(prompt, str)
    assert "AI" in prompt
    assert "Tech Summit" in prompt