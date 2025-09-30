from pydantic import BaseModel, Field
from typing import List, Optional

class EvaluateRequest(BaseModel):
    """Request model for content evaluation"""
    client_id: str = Field(default="default", description="Client application identifier")
    user: str = Field(default="anonymous", description="User identifier")
    input_type: str = Field(default="text", description="Type of input (text, image, file)")
    input: str = Field(..., description="Text content to evaluate")
    
    class Config:
        schema_extra = {
            "example": {
                "client_id": "app-1",
                "user": "alice",
                "input_type": "text",
                "input": "We will scrape faces from social media to build a facial recognition database"
            }
        }

class EvaluateResponse(BaseModel):
    """Response model for content evaluation"""
    decision: str = Field(..., description="Evaluation decision: allow, flag, or block")
    policy_tags: List[str] = Field(default=[], description="List of triggered policy tags")
    risk_level: str = Field(..., description="Risk level: unacceptable, high, limited, or minimal")
    audit_event_id: str = Field(..., description="Unique identifier for the audit event")
    explanation: str = Field(..., description="Human-readable explanation of the decision")
    confidence_score: int = Field(..., description="Confidence score (0-100)")
    policy_version: str = Field(..., description="Version of the policy pack used")
    
    class Config:
        schema_extra = {
            "example": {
                "decision": "block",
                "policy_tags": ["ProhibitedBiometric"],
                "risk_level": "unacceptable",
                "audit_event_id": "evt-20250128-abc12345",
                "explanation": "Blocked by ProhibitedBiometric: Real-time remote biometric identification & untargeted facial-database collection",
                "confidence_score": 85,
                "policy_version": "pack-2025-01-01-v1"
            }
        }
