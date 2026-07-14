from pydantic import BaseModel, Field
from typing import List, Optional


class ConversationRequest(BaseModel):
    """Schema for incoming conversation generation requests."""
    event_name: str = Field(..., description="Name of the networking event")
    user_role: str = Field(..., description="Professional role of the user")
    user_interests: List[str] = Field(
        default_factory=list,
        description="List of user interest keywords",
    )


class EventAnalysisRequest(BaseModel):
    """Schema for event analysis requests."""
    event_name: str = Field(..., description="Name of the networking event")
    user_role: str = Field(..., description="Professional role of the user")


class FactCheckRequest(BaseModel):
    """Schema for fact-check verification requests."""
    claims: List[str] = Field(..., description="List of claims to verify")


class FeedbackRequest(BaseModel):
    """Schema for user feedback submissions."""
    conversation_id: str = Field(..., description="ID of the conversation session")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    comments: Optional[str] = Field(default="", description="Optional feedback text")


class ThemeResult(BaseModel):
    """A single extracted theme with confidence score."""
    theme: str
    confidence: float


class EventAnalysisResponse(BaseModel):
    """Full event analysis result."""
    event_name: str
    user_role: str
    themes: List[ThemeResult]
    audience_profile: str



class TalkingPoint(BaseModel):
    """A single talking point within a topic."""
    point: str
    details: str


class TopicResponse(BaseModel):
    """A generated conversation topic with talking points."""
    topic: str
    talking_points: List[TalkingPoint]
    fact_check_status: str


class ConversationResponse(BaseModel):
    """Full conversation generation result."""
    conversation_id: str
    event_name: str
    topics: List[TopicResponse]
    timestamp: str



class FactCheckResult(BaseModel):
    """Verification result for a single claim."""
    claim: str
    verified: bool
    confidence: float
    source: str
    summary: str


class FactCheckResponse(BaseModel):
    """Aggregated fact-check results."""
    results: List[FactCheckResult]



class FeedbackResponse(BaseModel):
    """Acknowledgement after feedback submission."""
    status: str
    message: str