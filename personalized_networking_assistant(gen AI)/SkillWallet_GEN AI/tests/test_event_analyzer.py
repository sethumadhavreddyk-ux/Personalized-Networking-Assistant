import pytest
from app.services.event_analyzer import EventAnalyzer

def test_analyze_event_returns_dict():
    """Test that analyze_event returns a dictionary."""
    # We use a mocked/local instantiation or the mock fixture since it is globally overridden,
    # but we can test the real EventAnalyzer class behavior or stub it out as needed.
    # Note: EventAnalyzer requires loading model, so let's mock it inside this unit test file to run fast.
    from unittest.mock import MagicMock
    analyzer = EventAnalyzer.__new__(EventAnalyzer)
    analyzer.extract_themes = MagicMock(return_value=[{"theme": "Technology", "confidence": 0.95}])
    analyzer._determine_audience = MagicMock(return_value="Technical professionals")

    result = analyzer.analyze_event("Tech Summit", "Developer")
    assert isinstance(result, dict)
    assert result["event_name"] == "Tech Summit"
    assert result["user_role"] == "Developer"

def test_analyze_event_contains_required_keys():
    """Test that the analysis result contains required keys."""
    from unittest.mock import MagicMock
    analyzer = EventAnalyzer.__new__(EventAnalyzer)
    analyzer.extract_themes = MagicMock(return_value=[{"theme": "Technology", "confidence": 0.95}])
    analyzer._determine_audience = MagicMock(return_value="Technical professionals")

    result = analyzer.analyze_event("AI Expo", "Manager")
    assert "event_name" in result
    assert "user_role" in result
    assert "themes" in result
    assert "audience_profile" in result
def test_extract_themes_returns_list():
    """Test that extract_themes returns a list."""
    from unittest.mock import MagicMock
    import torch
    analyzer = EventAnalyzer.__new__(EventAnalyzer)
    analyzer.candidate_themes = ["Technology", "Business"]
    analyzer._theme_embeddings = torch.randn(2, 768)
    analyzer._compute_embeddings = MagicMock(return_value=torch.randn(1, 768))

    result = analyzer.extract_themes("Tech Summit")
    assert isinstance(result, list)


def test_extract_themes_non_empty():
    """Test that extracted themes list is not empty."""
    from unittest.mock import MagicMock
    import torch
    analyzer = EventAnalyzer.__new__(EventAnalyzer)
    analyzer.candidate_themes = ["Technology", "Business"]
    analyzer._theme_embeddings = torch.randn(2, 768)
    analyzer._compute_embeddings = MagicMock(return_value=torch.randn(1, 768))

    result = analyzer.extract_themes("Tech Summit")
    assert len(result) > 0
    assert "theme" in result[0]
    assert "confidence" in result[0]