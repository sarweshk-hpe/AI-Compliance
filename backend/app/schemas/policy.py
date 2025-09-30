from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class PolicyTagResponse(BaseModel):
    """Response model for policy tags"""
    id: int = Field(..., description="Policy tag ID")
    name: str = Field(..., description="Policy tag name")
    description: str = Field(..., description="Policy tag description")
    risk_level: str = Field(..., description="Risk level: unacceptable, high, limited, minimal")
    patterns: List[str] = Field(default=[], description="Patterns to match")
    action: str = Field(..., description="Action to take: block, flag, allow")
    policy_pack: str = Field(..., description="Policy pack name")

class PolicyPackResponse(BaseModel):
    """Response model for policy packs"""
    id: int = Field(..., description="Policy pack ID")
    name: str = Field(..., description="Policy pack name")
    version: str = Field(..., description="Policy pack version")
    description: str = Field(..., description="Policy pack description")
    is_active: bool = Field(..., description="Whether the pack is active")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
