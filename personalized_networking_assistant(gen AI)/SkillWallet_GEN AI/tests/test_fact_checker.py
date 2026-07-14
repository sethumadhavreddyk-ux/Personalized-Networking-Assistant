import pytest
from unittest.mock import patch, MagicMock
from app.services.fact_checker import FactChecker
@patch("app.services.fact_checker.wikipedia")
def test_check_facts_returns_list(mock_wiki):
    """Test that check_facts returns a list."""
    mock_wiki.search.return_value = ["AI"]
    mock_page = MagicMock()
    mock_page.url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    mock_page.summary = "Artificial intelligence is intelligence demonstrated by machines."
    mock_wiki.page.return_value = mock_page

    checker = FactChecker()
    result = checker.check_facts(["AI"])
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["verified"] is True


@patch("app.services.fact_checker.wikipedia")
def test_check_facts_contains_status(mock_wiki):
    """Test that each checked topic contains a fact-check status."""
    mock_wiki.search.return_value = ["AI"]
    mock_page = MagicMock()
    mock_page.url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    mock_page.summary = "Artificial intelligence is intelligence..."
    mock_wiki.page.return_value = mock_page

    checker = FactChecker()
    result = checker.check_facts(["AI"])
    assert len(result) > 0
    assert "verified" in result[0]
    assert "confidence" in result[0]

@patch("app.services.fact_checker.wikipedia")
def test_verify_claim_returns_dict(mock_wiki):
    """Test that verify_claim returns a dictionary."""
    mock_wiki.search.return_value = ["AI"]
    mock_page = MagicMock()
    mock_page.url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    mock_page.summary = "Artificial intelligence is intelligence..."
    mock_wiki.page.return_value = mock_page

    checker = FactChecker()
    result = checker.verify_claim("AI")
    assert isinstance(result, dict)
    assert result["claim"] == "AI"


@patch("app.services.fact_checker.wikipedia")
def test_verify_claim_contains_confidence(mock_wiki):
    """Test that verification result contains a confidence score."""
    mock_wiki.search.return_value = ["AI"]
    mock_page = MagicMock()
    mock_page.url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    mock_page.summary = "Artificial intelligence is intelligence..."
    mock_wiki.page.return_value = mock_page

    checker = FactChecker()
    result = checker.verify_claim("AI")
    assert "confidence" in result
    assert isinstance(result["confidence"], float)