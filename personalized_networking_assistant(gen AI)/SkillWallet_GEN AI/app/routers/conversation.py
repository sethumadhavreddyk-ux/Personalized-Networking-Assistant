
import uuid
from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    ConversationRequest,
    ConversationResponse,
    EventAnalysisRequest,
    EventAnalysisResponse,
    FactCheckRequest,
    FactCheckResponse,
    FeedbackRequest,
    FeedbackResponse,
    TopicResponse,
    TalkingPoint,
    ThemeResult,
    FactCheckResult,
)
from app.services.event_analyzer import EventAnalyzer
from app.services.topic_generator import TopicGenerator
from app.services.fact_checker import FactChecker
from app.services.history_logger import HistoryLogger
from app.services.feedback_logger import FeedbackLogger

router = APIRouter(tags=["conversation"])
_event_analyzer = None
_topic_generator = None
_fact_checker = None
_history_logger = None
_feedback_logger = None

def get_event_analyzer() -> EventAnalyzer:
    global _event_analyzer
    if _event_analyzer is None:
        _event_analyzer = EventAnalyzer()
    return _event_analyzer

def get_topic_generator() -> TopicGenerator:
    global _topic_generator
    if _topic_generator is None:
        _topic_generator = TopicGenerator()
    return _topic_generator

def get_fact_checker() -> FactChecker:
    global _fact_checker
    if _fact_checker is None:
        _fact_checker = FactChecker()
    return _fact_checker

def get_history_logger() -> HistoryLogger:
    global _history_logger
    if _history_logger is None:
        _history_logger = HistoryLogger()
    return _history_logger

def get_feedback_logger() -> FeedbackLogger:
    global _feedback_logger
    if _feedback_logger is None:
        _feedback_logger = FeedbackLogger()
    return _feedback_logger

@router.post("/generate-conversation", response_model=ConversationResponse)
async def generate_topics(request: ConversationRequest):
    """Generate personalized conversation topics for a networking event."""
    try:
        analyzer = get_event_analyzer()
        generator = get_topic_generator()
        checker = get_fact_checker()
        logger = get_history_logger()

        # Step 1: Analyze the event name and user role
        event_context = analyzer.analyze_event(request.event_name, request.user_role)

        # Step 2: Generate topics based on event context and user interests
        raw_topics = generator.generate_topics(event_context, request.user_interests)

        # Step 3: Fact-check topic themes
        topic_names = [t["topic"] for t in raw_topics]
        fact_results = checker.check_facts(topic_names)

        # Step 4: Map into response structure
        topics = []
        for raw, fact in zip(raw_topics, fact_results):
            status = "verified" if fact.get("verified") else "unverified"
            points = [
                TalkingPoint(point=tp.get("point", ""), details=tp.get("details", ""))
                for tp in raw.get("talking_points", [])
            ]
            topics.append(TopicResponse(
                topic=raw["topic"],
                talking_points=points,
                fact_check_status=status
            ))

        conversation_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()

        response = ConversationResponse(
            conversation_id=conversation_id,
            event_name=request.event_name,
            topics=topics,
            timestamp=timestamp
        )

        # Step 5: Log the generated session
        logger.log_conversation(response.model_dump())

        return response
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/analyze-event", response_model=EventAnalysisResponse)
async def analyze_event(request: EventAnalysisRequest):
    """Analyze event name and user role to identify themes."""
    try:
        analyzer = get_event_analyzer()
        result = analyzer.analyze_event(request.event_name, request.user_role)
        themes = [
            ThemeResult(theme=t["theme"], confidence=t["confidence"])
            for t in result.get("themes", [])
        ]
        return EventAnalysisResponse(
            event_name=result["event_name"],
            user_role=result["user_role"],
            themes=themes,
            audience_profile=result.get("audience_profile", "")
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/fact-check", response_model=FactCheckResponse)
async def fact_check(request: FactCheckRequest):
    """Verify factual accuracy of claims using Wikipedia."""
    try:
        checker = get_fact_checker()
        raw_results = checker.check_facts(request.claims)
        results = [
            FactCheckResult(
                claim=r["claim"],
                verified=r["verified"],
                confidence=r["confidence"],
                source=r["source"],
                summary=r["summary"]
            )
            for r in raw_results
        ]
        return FactCheckResponse(results=results)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/history", response_model=List[ConversationResponse])
async def get_history():
    """Retrieve past conversation history."""
    try:
        logger = get_history_logger()
        history = logger.get_history()
        # Parse history items back to list of ConversationResponse
        validated_history = []
        for item in history:
            try:
                # filter out any non-schema fields
                validated_history.append(ConversationResponse(**item))
            except Exception:
                continue
        return validated_history
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest):
    """Submit user feedback for a conversation session."""
    try:
        logger = get_feedback_logger()
        logger.log_feedback(request.model_dump())
        return FeedbackResponse(
            status="success",
            message="Feedback logged successfully."
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/feedback")
async def get_feedback():
    """Retrieve all submitted feedback entries."""
    try:
        logger = get_feedback_logger()
        return logger.get_feedback()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))