from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class AuditEventResponse(BaseModel):
    """Response model for audit events"""
    event_id: str = Field(..., description="Unique event identifier")
    timestamp: datetime = Field(..., description="Event timestamp")
    user: str = Field(..., description="User who triggered the event")
    client_id: str = Field(..., description="Client application identifier")
    input_type: str = Field(..., description="Type of input evaluated")
    decision: str = Field(..., description="Evaluation decision")
    policy_tags: List[str] = Field(default=[], description="Triggered policy tags")
    risk_level: str = Field(..., description="Risk level assessment")
    policy_version: str = Field(..., description="Policy version used")
    explanation: str = Field(..., description="Human-readable explanation")
    confidence_score: int = Field(..., description="Confidence score (0-100)")
    signature: str = Field(..., description="HMAC signature for integrity")

class AuditOverrideRequest(BaseModel):
    """Request model for creating audit overrides"""
    operator: str = Field(..., description="Operator performing the override")
    reason: str = Field(..., description="Reason for the override")
    new_decision: str = Field(..., description="New decision after override")
    duration: Optional[int] = Field(None, description="Override duration in minutes")

class AuditOverrideResponse(BaseModel):
    """Response model for audit overrides"""
    override_id: str = Field(..., description="Unique override identifier")
    original_event_id: str = Field(..., description="Original event being overridden")
    timestamp: datetime = Field(..., description="Override timestamp")
    operator: str = Field(..., description="Operator who performed the override")
    reason: str = Field(..., description="Reason for the override")
    new_decision: str = Field(..., description="New decision after override")
    duration: Optional[int] = Field(None, description="Override duration in minutes")
    signature: str = Field(..., description="HMAC signature for integrity")
