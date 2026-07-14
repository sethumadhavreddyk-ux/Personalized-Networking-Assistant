
import pytest
def test_generate_topics_status_code(test_client, sample_conversation_request):
    """Test that the generate topics endpoint returns 200."""
    response = test_client.post("/generate-conversation", json=sample_conversation_request)
    assert response.status_code == 200


def test_generate_topics_response_structure(test_client, sample_conversation_request):
    """Test that the response contains expected fields."""
    response = test_client.post("/generate-conversation", json=sample_conversation_request)
    assert response.status_code == 200
    json_data = response.json()
    assert "conversation_id" in json_data
    assert "event_name" in json_data
    assert "topics" in json_data
    assert "timestamp" in json_data
    assert json_data["event_name"] == "Tech Summit 2026"
def test_analyze_event_status_code(test_client, sample_event_context):
    """Test that the analyze-event endpoint returns 200 and correct structure."""
    payload = {
        "event_name": sample_event_context["event_name"],
        "user_role": sample_event_context["user_role"]
    }
    response = test_client.post("/analyze-event", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    assert "audience_profile" in json_data
    assert "themes" in json_data

def test_fact_check_endpoint(test_client):
    """Test that the fact-check endpoint validates claims successfully."""
    payload = {
        "claims": ["Quantum Computing", "Deep Learning"]
    }
    response = test_client.post("/fact-check", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    assert "results" in json_data
    assert len(json_data["results"]) == 2
    assert json_data["results"][0]["claim"] == "Quantum Computing"

def test_get_history_status_code(test_client):
    """Test that the history endpoint returns 200."""
    response = test_client.get("/history")
    assert response.status_code == 200


def test_get_history_returns_list(test_client):
    """Test that the history endpoint returns a list."""
    response = test_client.get("/history")
    assert response.status_code == 200
    json_data = response.json()
    assert isinstance(json_data, list)

def test_submit_feedback_status_code(test_client, sample_feedback_request):
    """Test that the feedback endpoint returns 200."""
    response = test_client.post("/feedback", json=sample_feedback_request)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "success"


def test_get_feedback_returns_list(test_client):
    """Test that the get feedback endpoint returns a list."""
    response = test_client.get("/feedback")
    assert response.status_code == 200
    json_data = response.json()
    assert isinstance(json_data, list)